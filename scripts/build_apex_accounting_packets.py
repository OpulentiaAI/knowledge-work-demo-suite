#!/usr/bin/env python3
"""Build five pinned Mercor APEX-Accounting development-set packets."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
DATASET = "Mercor APEX-Accounting Dev Set"
UPSTREAM_REPO = "mercor/apex-accounting"
UPSTREAM_COMMIT = "bf5e8c99117b7ee763d79ad2c64563ac844d77d2"
UPSTREAM_BASE = (
    "https://huggingface.co/datasets/"
    f"{UPSTREAM_REPO}/resolve/{UPSTREAM_COMMIT}"
)
USER_AGENT = "knowledge-work-demo-suite/1.0"


TASKS: list[dict[str, Any]] = [
    {
        "id": "054-apex-accounting-contingency-settlement-je",
        "upstream_id": "task_baa139877a4d4fbfa601df50610262d5",
        "upstream_file": "world_9_task_04.json",
        "title": "Propose a Contingency Settlement Journal Entry",
        "domain": "accounting-data-entry",
        "source_paths": [
            "world/filesystem/workpaper_contingency_case_status_2024.xlsx",
            "world/filesystem/workpaper_client_cost_advance_ledger_2024.xlsx",
            "world/apps_data/quickbooks/qbo_journal_entry_register_2024.xlsx",
            "world/filesystem/workpaper_whitfield_settlement_summary.xlsx",
            "task_files/world_9_task_04/Whitfield_PostSettlement_Holdback_Memo.pdf",
        ],
    },
    {
        "id": "055-apex-accounting-payroll-reconciliation",
        "upstream_id": "task_848b939d069a4378b3e6e1d989aca7fc",
        "upstream_file": "world_9_task_05.json",
        "title": "Reconcile December Payroll Between Gusto and QBO",
        "domain": "payroll-accounting",
        "source_paths": [
            "world/filesystem/gusto_payroll_register_2024.csv",
            "world/filesystem/qbo_general_ledger_detail_2024.xlsx",
            "world/filesystem/workpaper_payroll_accrual_2024_12_31.xlsx",
            "world/filesystem/workpaper_pto_accrual_2024_12_31.xlsx",
            "world/filesystem/attorney_staff_roster.xlsx",
            "world/filesystem/partner_compensation_schedule.xlsx",
            "world/filesystem/gusto_employee_earnings_summary_2024.xlsx",
            "task_files/world_9_task_05/Controller Memo 12_31.txt",
        ],
    },
    {
        "id": "056-apex-accounting-year-end-wip-rollforward",
        "upstream_id": "task_55332112bcb94ff4b489844dba2d91e0",
        "upstream_file": "world_9_task_07.json",
        "title": "Finalize the Year-End Unbilled WIP Rollforward",
        "domain": "revenue-accounting",
        "source_paths": [
            "world/filesystem/workpaper_realization_rate_analysis_2024.xlsx",
            "world/apps_data/quickbooks/clio_billing_export_2024.csv",
            "world/filesystem/engagement_letter_summary_2024.xlsx",
            "task_files/world_9_task_07/T1_Year_End_WIP_Schedule.pdf",
            "task_files/world_9_task_07/Year_End_WIP_Realization_Methodology_Memo.pdf",
            "task_files/world_9_task_07/Year_End_Matter_Status_Update.pdf",
        ],
    },
    {
        "id": "057-apex-accounting-ar-reconciliation",
        "upstream_id": "task_3155ba0f5d37465cb051c89ead5ec9bb",
        "upstream_file": "world_9_task_13.json",
        "title": "Finalize the Clio-to-QBO Accounts Receivable Reconciliation",
        "domain": "accounts-receivable",
        "source_paths": [
            "world/apps_data/quickbooks/clio_billing_export_2024.csv",
            "world/filesystem/qbo_ar_aging_summary_2024_12_31.xlsx",
            "world/filesystem/qbo_general_ledger_detail_2024.xlsx",
            "task_files/world_9_task_13/Draft_AR_Reconciliation_Clio_QBO_Dec_2024.xlsx",
            "task_files/world_9_task_13/Senior_Review_Notes_Dec_2024.pdf",
        ],
    },
    {
        "id": "058-apex-accounting-collections-variance",
        "upstream_id": "task_6140e09e1ce6482c8b4cfcdc007f758c",
        "upstream_file": "world_9_task_23.json",
        "title": "Analyze Monthly Collections Variance by Practice Group",
        "domain": "accounting-variance-analysis",
        "source_paths": [
            "world/filesystem/client_matter_list.xlsx",
            "world/apps_data/quickbooks/clio_billing_export_2024.csv",
            "task_files/world_9_task_23/Management Memo.docx",
        ],
    },
]


def request_bytes(url: str, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                payload = response.read()
            if not payload:
                raise RuntimeError(f"Downloaded an empty file from {url}")
            return payload
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if attempt == attempts:
                raise RuntimeError(f"Failed to download {url}: {error}") from error
            time.sleep(attempt * 1.5)
    raise AssertionError("unreachable")


def upstream_url(relative: str) -> str:
    return f"{UPSTREAM_BASE}/{urllib.parse.quote(relative, safe='/')}"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )


def build_task(
    selected: dict[str, Any],
    upstream_task: dict[str, Any],
    license_bytes: bytes,
) -> None:
    task_dir = TASKS_DIR / selected["id"]
    if task_dir.exists():
        shutil.rmtree(task_dir)
    source_dir = task_dir / "source_docs"
    source_dir.mkdir(parents=True)

    context_names = upstream_task["context_files"]
    selected_names = [Path(path).name for path in selected["source_paths"]]
    if selected_names != context_names:
        raise RuntimeError(
            f"{selected['id']}: configured source paths do not match context_files"
        )
    if len(selected_names) != len(set(selected_names)):
        raise RuntimeError(f"{selected['id']}: duplicate flattened source filename")

    for relative in selected["source_paths"]:
        (source_dir / Path(relative).name).write_bytes(
            request_bytes(upstream_url(relative))
        )
    (source_dir / "UPSTREAM_LICENSE").write_bytes(license_bytes)
    (source_dir / "SOURCE_PROVENANCE.md").write_text(
        f"""# Source provenance

- Dataset: `{UPSTREAM_REPO}`
- Revision: `{UPSTREAM_COMMIT}`
- World: `{upstream_task['world_id']}`
- License: Creative Commons Attribution 4.0 International
- Dataset URL: https://huggingface.co/datasets/{UPSTREAM_REPO}

The working files are byte-exact copies from the pinned public development-set
revision. The upstream filesystem and task-specific directories are flattened
here to match the runtime layout described by the dataset publisher.
""",
        encoding="utf-8",
    )
    packet_files = sorted(
        path
        for path in source_dir.iterdir()
        if path.is_file() and path.name != "SOURCE_FILES.sha256"
    )
    (source_dir / "SOURCE_FILES.sha256").write_text(
        "\n".join(f"{sha256(path)}  {path.name}" for path in packet_files) + "\n",
        encoding="utf-8",
    )

    (task_dir / "prompt.md").write_text(
        f"""# {selected['title']}

## Assignment

{upstream_task['prompt'].strip()}

## Source documents

Use the files under `source_docs/` as the authoritative company workspace.
Do not use internet lookup or modify the source files.

## Expected deliverable

Write the exact response you would submit to the accounting console to:

- `answer.txt`
""",
        encoding="utf-8",
    )

    normalized = {
        "id": selected["id"],
        "title": selected["title"],
        "domain": selected["domain"],
        "work_type": "cross-document-accounting-analysis",
        "dataset": DATASET,
        "upstream_id": selected["upstream_id"],
        "upstream_url": (
            "https://huggingface.co/datasets/"
            f"{UPSTREAM_REPO}/blob/{UPSTREAM_COMMIT}/tasks/{selected['upstream_file']}"
        ),
        "license": "CC-BY-4.0",
        "attribution": "Mercor and Ramp, APEX-Accounting public development set",
        "prompt": "prompt.md",
        "source_docs": "source_docs",
        "deliverables": ["answer.txt"],
        "rubric": "rubric.json",
        "apex_accounting_config": "apex_accounting.json",
    }
    write_json(task_dir / "task.json", normalized)
    write_json(task_dir / "rubric.json", upstream_task["rubric"])
    write_json(task_dir / "upstream_task.json", upstream_task)
    write_json(
        task_dir / "apex_accounting.json",
        {
            "schema_version": "1.0",
            "profile": "apex-accounting-static-dev-v1",
            "dataset_repository": UPSTREAM_REPO,
            "dataset_commit": UPSTREAM_COMMIT,
            "world_id": upstream_task["world_id"],
            "source_mode": "task-required static exports, flattened",
            "read_only": True,
            "network": "disabled",
            "answer_file": "answer.txt",
            "grading": {
                "mode": "binary criterion review of final answer",
                "criteria_file": "rubric.json",
                "gold_file": "answer_key.md",
                "trajectory_used": False,
            },
            "blind_run": {
                "agent_visible": [
                    "prompt.md",
                    "task.json",
                    "apex_accounting.json",
                    "source_docs/",
                ],
                "grader_hidden": [
                    "rubric.json",
                    "answer_key.md",
                    "upstream_task.json",
                ],
            },
            "output": {"required_files": ["answer.txt"]},
        },
    )
    (task_dir / "answer_key.md").write_text(
        f"""# Grader answer key — {selected['id']}

Keep this file hidden from the agent during a blind run.

## Upstream expert response

{upstream_task['gold_output'].strip()}
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()

    records = [
        json.loads(line)
        for line in request_bytes(upstream_url("data/dev.jsonl"))
        .decode("utf-8")
        .splitlines()
        if line.strip()
    ]
    by_id = {record["task_id"]: record for record in records}
    if len(records) != 10:
        raise RuntimeError(f"Expected 10 public dev tasks, found {len(records)}")
    license_bytes = request_bytes(upstream_url("LICENSE"))
    for selected in TASKS:
        upstream_task = by_id.get(selected["upstream_id"])
        if upstream_task is None:
            raise RuntimeError(f"Missing upstream task: {selected['upstream_id']}")
        build_task(selected, upstream_task, license_bytes)
        print(f"Built {selected['id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
