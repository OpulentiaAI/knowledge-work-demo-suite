#!/usr/bin/env python3
"""Build compact agent-facing diagnostic packets from the public POS export.

The source dataset is Mendeley Data DOI 10.17632/39xdjxgnmf.1. This script
deliberately writes only observed sales metrics and calendar labels into each
task packet; generator multipliers and the full event truth are evaluator
artifacts, not agent inputs.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
TASKS = {
    "021-synthetic-post-holiday-sales": {
        "store": "Store 04 - San Antonio",
        "target": ("2024-01-02", "2024-01-06"),
        "baseline": ("2024-01-09", "2024-01-13"),
        "calendar": {
            "2024-01-02": "Post-holiday returns period",
            "2024-01-03": "Post-holiday returns period",
            "2024-01-04": "Post-holiday returns period",
            "2024-01-05": "Post-holiday returns period",
            "2024-01-06": "Post-holiday returns period",
        },
    },
    "022-synthetic-valentine-sales": {
        "store": "Store 09 - Chicago",
        "target": ("2024-02-13", "2024-02-14"),
        "baseline": ("2024-02-06", "2024-02-07"),
        "calendar": {
            "2024-02-13": "Valentine's Eve",
            "2024-02-14": "Valentine's Day",
        },
    },
    "023-synthetic-easter-sales": {
        "store": "Store 18 - Memphis",
        "target": ("2024-03-31", "2024-03-31"),
        "baseline": ("2024-03-24", "2024-03-24"),
        "calendar": {"2024-03-31": "Easter Sunday"},
    },
}


def metric_frames(detail: pd.DataFrame, dates: list[pd.Timestamp]) -> tuple[pd.DataFrame, pd.DataFrame]:
    subset = detail[detail["Date"].isin(dates)].copy()
    payments = subset[subset["Event Type"].eq("Payment")]
    refunds = subset[subset["Event Type"].eq("Refund")]

    payment_daily = payments.groupby(["Date", "Location"], as_index=False).agg(
        **{
            "Gross Sales": ("Gross Sales", "sum"),
            "Payment Net Sales": ("Net Sales", "sum"),
            "Discounts": ("Discounts", "sum"),
            "Gross Profit": ("Gross Profit", "sum"),
            "Transactions": ("Transaction ID", "nunique"),
            "Units": ("Qty", "sum"),
        }
    )
    refund_daily = refunds.groupby(["Date", "Location"], as_index=False).agg(
        **{
            "Refund Net Sales": ("Net Sales", "sum"),
            "Refund Transactions": ("Transaction ID", "nunique"),
        }
    )
    daily = payment_daily.merge(refund_daily, how="left", on=["Date", "Location"]).fillna(0)
    daily["Net Sales After Refunds"] = daily["Payment Net Sales"] + daily["Refund Net Sales"]
    daily["Discount Rate"] = -daily["Discounts"] / daily["Gross Sales"]
    daily["Average Payment Net Basket"] = daily["Payment Net Sales"] / daily["Transactions"]

    category_daily = payments.groupby(["Date", "Location", "Category"], as_index=False).agg(
        **{
            "Payment Net Sales": ("Net Sales", "sum"),
            "Gross Profit": ("Gross Profit", "sum"),
            "Units": ("Qty", "sum"),
            "Transactions": ("Transaction ID", "nunique"),
        }
    )
    return daily, category_daily


def write_packet(task_id: str, config: dict[str, object], detail: pd.DataFrame) -> None:
    task_dir = ROOT / "tasks" / task_id
    source_dir = task_dir / "source_docs"
    source_dir.mkdir(parents=True, exist_ok=True)
    target_start, target_end = config["target"]
    baseline_start, baseline_end = config["baseline"]
    dates = list(
        pd.date_range(target_start, target_end).union(pd.date_range(baseline_start, baseline_end))
    )
    daily, categories = metric_frames(detail, dates)
    daily["Period"] = daily["Date"].between(target_start, target_end).map(
        {True: "diagnostic", False: "comparison"}
    )
    daily["Date"] = daily["Date"].dt.strftime("%Y-%m-%d")
    daily.sort_values(["Date", "Location"]).to_csv(source_dir / "daily_store_metrics.csv", index=False)

    target_categories = categories[categories["Location"].eq(config["store"])].copy()
    target_categories["Period"] = target_categories["Date"].between(target_start, target_end).map(
        {True: "diagnostic", False: "comparison"}
    )
    target_categories["Date"] = target_categories["Date"].dt.strftime("%Y-%m-%d")
    target_categories.sort_values(["Date", "Category"]).to_csv(
        source_dir / "target_store_category_metrics.csv", index=False
    )

    calendar = pd.DataFrame({"Date": [date.strftime("%Y-%m-%d") for date in dates]})
    calendar["Weekday"] = pd.to_datetime(calendar["Date"]).dt.day_name()
    labels = config["calendar"]
    calendar["Retail calendar observation"] = calendar["Date"].map(labels).fillna("No named retail-calendar observation")
    calendar["Period"] = calendar["Date"].between(target_start, target_end).map(
        {True: "diagnostic", False: "comparison"}
    )
    calendar.to_csv(source_dir / "retail_calendar.csv", index=False)

    (source_dir / "data_dictionary.md").write_text(
        "# Sales packet data dictionary\n\n"
        "`daily_store_metrics.csv` contains one row per store and date. Sales and profit are USD. "
        "`Payment Net Sales` covers payment line items; `Refund Net Sales` is negative; `Net Sales After Refunds` "
        "combines both. `Discounts` is negative in the source export, so `Discount Rate` is shown as a positive share. "
        "A transaction is counted once per payment transaction ID.\n\n"
        "`target_store_category_metrics.csv` contains payment-only metrics by category for the named target store. "
        "`retail_calendar.csv` provides calendar context, not causal proof.\n"
    )
    (source_dir / "provenance.md").write_text(
        "# Provenance\n\n"
        "These packet files are deterministic aggregates of the public *A Synthetic Multi-Store Retail "
        "Point-of-Sale Transaction Dataset in Square POS Export Format*, Mendeley Data DOI "
        "[10.17632/39xdjxgnmf.1](https://doi.org/10.17632/39xdjxgnmf.1), published July 13, 2026. "
        "The upstream dataset is CC BY 4.0. The packets retain observed sales, discount, refund, profit, "
        "store, category, and calendar fields needed for analysis; they intentionally omit the generator's "
        "event multipliers and other answer-key parameters.\n"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("detail_csv", type=Path, help="Path to 01_square_item_sales_detail_24mo.csv")
    args = parser.parse_args()
    detail = pd.read_csv(args.detail_csv, parse_dates=["Date"])
    for task_id, config in TASKS.items():
        write_packet(task_id, config, detail)


if __name__ == "__main__":
    main()
