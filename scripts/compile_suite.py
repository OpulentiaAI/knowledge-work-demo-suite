#!/usr/bin/env python3
"""Compile a 20-task professional knowledge-work demo suite from live sources."""

from __future__ import annotations

import argparse
import csv
import hashlib
import html
import json
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
SOURCE_POOLS_DIR = ROOT / "source_pools"
MANIFESTS_DIR = ROOT / "manifests"
USER_AGENT = "knowledge-work-demo-suite/1.0"

AA_REPO = "https://huggingface.co/datasets/ArtificialAnalysis/AA-Briefcase-Lite"
GDP_REPO = "https://huggingface.co/datasets/openai/gdpval"
WORKSPACE_REPO = "https://huggingface.co/datasets/Workspace-Bench/Workspace-Bench-Lite"
HARVEY_RAW = "https://raw.githubusercontent.com/OpulentiaAI/harvey-labs/main"

AA_TASKS = [
    ("001-aa-market-overview", "w1_t1", "Market Structure and Competitive Landscape", "commercial-diligence"),
    ("002-aa-market-model", "w1_t2", "Market Sizing, Forecast, and Cage-Ban Transition Model", "financial-modeling"),
    ("003-aa-target-assessment", "w1_t3", "Target Assessment, Opportunities, and Risks", "strategy"),
    ("004-aa-findings-briefing", "w1_t4", "Preliminary Findings Executive Briefing", "executive-communication"),
]

HARVEY_TASKS = [
    {
        "dir": "005-harvey-ma-red-flags",
        "path": "corporate-ma/review-data-room-red-flag-review",
        "domain": "legal-ma-diligence",
        "documents": [
            "confidential-information-memorandum.docx",
            "credit-agreement-summary.docx",
            "customer-contract-summary.xlsx",
            "employee-benefits-summary.docx",
            "employment-agreements-summary.docx",
            "environmental-permit-schedule.docx",
            "executed-loi.docx",
            "insurance-program-summary.docx",
            "litigation-regulatory-summary.docx",
            "org-chart-equity-structure.docx",
            "phase-ii-esa-executive-summary.docx",
            "qoe-data-request-response.xlsx",
            "real-property-lease-schedule.docx",
        ],
    },
    {
        "dir": "006-harvey-real-estate-psa",
        "path": "real-estate/extract-psa-key-terms/scenario-01",
        "domain": "legal-real-estate",
        "documents": [
            "gc-instruction-email.eml",
            "phase-i-esa-executive-summary.docx",
            "purchase-and-sale-agreement.docx",
        ],
    },
    {
        "dir": "007-harvey-nda-playbook",
        "path": "corporate-governance/review-nda-playbook-review",
        "domain": "legal-contract-review",
        "documents": [
            "datapulse-draft-nda.docx",
            "deal-team-cover-email.eml",
            "hightower-nda-playbook.docx",
        ],
    },
    {
        "dir": "008-harvey-dip-motion",
        "path": "bankruptcy-restructuring/draft-dip-financing-motion",
        "domain": "legal-bankruptcy",
        "documents": [
            "13-week-cash-flow.xlsx",
            "broadmoor-appraisal-summary.docx",
            "del-bankr-dip-guidelines.docx",
            "dip-marketing-emails.eml",
            "dip-term-sheet.docx",
            "ferris-declaration.docx",
            "lien-search-summary.docx",
            "prepetition-credit-agreement.docx",
        ],
    },
    {
        "dir": "009-harvey-litigation-assessment",
        "path": "litigation-dispute-resolution/draft-case-assessment-memorandum",
        "domain": "legal-litigation",
        "documents": [
            "bridger-damages-report.docx",
            "cascade-complaint.docx",
            "cascade-forensic-summary.docx",
            "cascade-rejection-letter.docx",
            "distribution-agreement.docx",
            "greenleaf-internal-emails.eml",
            "jantzen-employment-agreement.docx",
            "termination-letter.docx",
        ],
    },
    {
        "dir": "010-harvey-cross-border-tax",
        "path": "tax/draft-cross-border-acquisition-tax-memo",
        "domain": "legal-tax",
        "documents": [
            "country-by-country-report-fy2022-and-fy2023.docx",
            "dac6-analysis-memo-internal-draft-incomplete.docx",
            "draft-share-purchase-agreement-spa.docx",
            "due-diligence-tax-report-ernst-young.docx",
            "dutch-local-tax-opinion.docx",
            "financial-model-tax-analysis-tab.docx",
            "financial-model-transaction-overview-tab.docx",
            "financial-model-transfer-pricing-tab.docx",
            "german-local-tax-opinion.docx",
            "group-corporate-structure-chart-pre-acquisition-narrative-description.docx",
            "hargrove-lund-fee-estimate-and-engagement-letter.docx",
            "intercompany-loan-agreement-nordenvik-holding-gmbh-to-nordenvik-group-ab.docx",
            "ip-assignment-agreements-nordenvik-ab-to-nordenvik-bv.docx",
            "master-file-transfer-pricing.docx",
            "nordenvik-group-ab-consolidated-financial-statements-fy2023.docx",
            "post-close-integration-plan-tax-section-extract.docx",
            "proposed-acquisition-structure-chart-post-acquisition-narrative-description.docx",
            "representations-warranties-insurance-rwi-coverage-binder.docx",
            "singapore-local-tax-opinion.docx",
            "swedish-local-tax-opinion.docx",
            "term-sheet-acquisition-financing.docx",
            "updated-transfer-pricing-study-kpmg.docx",
        ],
    },
]

GDP_TASKS = [
    ("011-gdpval-energy-portfolio-risk", "46b34f78-6c06-4416-87e2-77b6d8b20ce9", "quantitative-finance"),
    ("012-gdpval-materials-lab", "8077e700-2b31-402d-bd09-df4d33c39653", "mechanical-engineering"),
    ("013-gdpval-dialysis-lab-management", "90edba97-74f0-425a-8ff6-8b93182eb7cb", "healthcare"),
    ("014-gdpval-ai-project-controls", "3c19c6d1-672c-467a-8437-6fe21afb8eae", "project-management"),
    ("015-gdpval-regional-sales-analysis", "a69be28f-9a84-47c9-992e-b90446cdca9d", "sales"),
    ("016-gdpval-cloud-modernization", "a45bc83b-22f9-4def-8d89-9c5661b2b86f", "systems-architecture"),
]

WORKSPACE_TASKS = [
    ("017-workspace-product-expense-analysis", "15", "product-management"),
    ("018-workspace-emergency-operations", "72", "logistics-operations"),
    ("019-workspace-global-product-strategy", "107", "global-operations"),
    ("020-workspace-llm-memory-survey", "363", "research"),
]


def request_bytes(url: str, attempts: int = 4) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    for attempt in range(1, attempts + 1):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                return response.read()
        except (urllib.error.URLError, TimeoutError, ConnectionError) as error:
            if attempt == attempts:
                raise RuntimeError(f"Failed to download {url}: {error}") from error
            time.sleep(attempt * 1.5)
    raise AssertionError("unreachable")


def get_json(url: str) -> Any:
    return json.loads(request_bytes(url).decode("utf-8"))


def download(url: str, destination: Path, refresh: bool) -> None:
    if destination.is_file() and destination.stat().st_size > 0 and not refresh:
        return
    destination.parent.mkdir(parents=True, exist_ok=True)
    payload = request_bytes(url)
    if not payload:
        raise RuntimeError(f"Downloaded an empty file from {url}")
    temporary = destination.with_name(destination.name + ".part")
    temporary.write_bytes(payload)
    temporary.replace(destination)


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def write_prompt(path: Path, title: str, assignment: str, deliverables: list[str]) -> None:
    outputs = "\n".join(f"- `{name}`" for name in deliverables)
    content = (
        f"# {title}\n\n"
        "## Assignment\n\n"
        f"{assignment.strip()}\n\n"
        "## Source documents\n\n"
        "Use the files in `source_docs/`. Treat them as the authoritative task workspace.\n\n"
        "## Expected deliverables\n\n"
        f"{outputs}\n"
    )
    path.write_text(content, encoding="utf-8")


def parse_json_field(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    stripped = value.strip()
    if not stripped:
        return []
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        return value


def basename_from_upstream(path: str) -> str:
    return Path(urllib.parse.unquote(path)).name


def compile_aa(refresh: bool) -> list[dict[str, Any]]:
    print("Compiling AA-Briefcase-Lite...")
    api_tree = get_json(
        "https://huggingface.co/api/datasets/ArtificialAnalysis/AA-Briefcase-Lite/"
        "tree/main?recursive=true&expand=false"
    )
    source_files = [
        entry["path"]
        for entry in api_tree
        if entry.get("type") == "file" and entry["path"].startswith("source_files/")
    ]
    pool = SOURCE_POOLS_DIR / "aa-briefcase-lite"
    for relative in source_files:
        encoded = urllib.parse.quote(relative, safe="/")
        destination = pool / Path(relative).relative_to("source_files")
        download(f"{AA_REPO}/resolve/main/{encoded}", destination, refresh)

    tasks_rows = [
        json.loads(line)
        for line in request_bytes(f"{AA_REPO}/resolve/main/tasks.jsonl").decode("utf-8").splitlines()
        if line.strip()
    ]
    task_by_id = {row["task_id"]: row for row in tasks_rows}
    checks = [
        json.loads(line)
        for line in request_bytes(f"{AA_REPO}/resolve/main/checks.jsonl").decode("utf-8").splitlines()
        if line.strip()
    ]

    records: list[dict[str, Any]] = []
    for directory, upstream_id, title, domain in AA_TASKS:
        row = task_by_id[upstream_id]
        task_dir = TASKS_DIR / directory
        task_dir.mkdir(parents=True, exist_ok=True)
        prompt_url = f"{AA_REPO}/resolve/main/{urllib.parse.quote(row['task_md_path'], safe='/')}"
        download(prompt_url, task_dir / "prompt.md", refresh)
        source_link = task_dir / "source_docs"
        if source_link.exists() and not source_link.is_symlink():
            raise RuntimeError(f"Expected symlink at {source_link}")
        if source_link.is_symlink():
            source_link.unlink()
        source_link.symlink_to(Path("../../source_pools/aa-briefcase-lite"))
        rubric_rows = [check for check in checks if check.get("task_id") == upstream_id]
        (task_dir / "rubric.jsonl").write_text(
            "".join(json.dumps(item, ensure_ascii=False) + "\n" for item in rubric_rows),
            encoding="utf-8",
        )
        normalized = {
            "id": directory,
            "title": title,
            "domain": domain,
            "work_type": "analyze-and-create",
            "dataset": "AA-Briefcase-Lite",
            "upstream_id": upstream_id,
            "upstream_url": f"{AA_REPO}/blob/main/{row['task_md_path']}",
            "license": "Apache-2.0",
            "prompt": "prompt.md",
            "source_docs": "source_docs",
            "deliverables": row["deliverable_filenames"],
            "rubric": "rubric.jsonl",
        }
        write_json(task_dir / "task.json", normalized)
        write_json(task_dir / "upstream_task.json", row)
        records.append(normalized)
    return records


def compile_harvey(refresh: bool) -> list[dict[str, Any]]:
    print("Compiling Harvey LAB...")
    records: list[dict[str, Any]] = []
    for selected in HARVEY_TASKS:
        task_path = selected["path"]
        encoded_task_path = urllib.parse.quote(task_path, safe="/")
        upstream = get_json(f"{HARVEY_RAW}/tasks/{encoded_task_path}/task.json")
        task_dir = TASKS_DIR / selected["dir"]
        source_dir = task_dir / "source_docs"
        source_dir.mkdir(parents=True, exist_ok=True)
        for filename in selected["documents"]:
            encoded_name = urllib.parse.quote(filename)
            download(
                f"{HARVEY_RAW}/tasks/{encoded_task_path}/documents/{encoded_name}",
                source_dir / filename,
                refresh,
            )
        deliverables_value = upstream.get("deliverables", {})
        deliverables = (
            list(deliverables_value)
            if isinstance(deliverables_value, dict)
            else list(deliverables_value or [])
        )
        write_prompt(
            task_dir / "prompt.md",
            upstream["title"],
            upstream["instructions"],
            deliverables,
        )
        write_json(task_dir / "rubric.json", upstream.get("criteria", []))
        write_json(task_dir / "upstream_task.json", upstream)
        normalized = {
            "id": selected["dir"],
            "title": upstream["title"],
            "domain": selected["domain"],
            "work_type": upstream.get("work_type", "knowledge-work"),
            "dataset": "Harvey Legal Agent Benchmark",
            "upstream_id": task_path,
            "upstream_url": f"https://github.com/OpulentiaAI/harvey-labs/tree/main/tasks/{task_path}",
            "license": "MIT",
            "prompt": "prompt.md",
            "source_docs": "source_docs",
            "deliverables": deliverables,
            "rubric": "rubric.json",
        }
        write_json(task_dir / "task.json", normalized)
        records.append(normalized)
    return records


def load_gdp_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for offset, length in ((0, 100), (100, 100), (200, 100)):
        url = (
            "https://datasets-server.huggingface.co/rows"
            "?dataset=openai%2Fgdpval&config=default&split=train"
            f"&offset={offset}&length={length}"
        )
        payload = get_json(url)
        rows.extend(item["row"] for item in payload["rows"])
    return rows


def compile_gdpval(refresh: bool) -> list[dict[str, Any]]:
    print("Compiling OpenAI GDPval...")
    by_id = {row["task_id"]: row for row in load_gdp_rows()}
    records: list[dict[str, Any]] = []
    for directory, upstream_id, domain in GDP_TASKS:
        row = by_id[upstream_id]
        task_dir = TASKS_DIR / directory
        source_dir = task_dir / "source_docs"
        source_dir.mkdir(parents=True, exist_ok=True)
        for relative, url in zip(row["reference_files"], row["reference_file_urls"]):
            download(url, source_dir / basename_from_upstream(relative), refresh)
        deliverables = [basename_from_upstream(path) for path in row["deliverable_files"]]
        title = f"{row['occupation']}: {domain.replace('-', ' ').title()}"
        write_prompt(task_dir / "prompt.md", title, row["prompt"], deliverables)
        rubric = parse_json_field(row.get("rubric_json", []))
        write_json(task_dir / "rubric.json", rubric)
        write_json(task_dir / "upstream_task.json", row)
        normalized = {
            "id": directory,
            "title": title,
            "domain": domain,
            "work_type": "professional-deliverable",
            "sector": row["sector"],
            "occupation": row["occupation"],
            "dataset": "OpenAI GDPval",
            "upstream_id": upstream_id,
            "upstream_url": f"{GDP_REPO}?row={upstream_id}",
            "license": "Upstream terms apply; no standardized license declared in dataset card",
            "prompt": "prompt.md",
            "source_docs": "source_docs",
            "deliverables": deliverables,
            "rubric": "rubric.json",
        }
        write_json(task_dir / "task.json", normalized)
        records.append(normalized)
    return records


def load_workspace_rows() -> list[dict[str, str]]:
    url = f"{WORKSPACE_REPO}/resolve/main/task_lite_clean_en_metadata_table.csv"
    content = request_bytes(url).decode("utf-8-sig").splitlines()
    return list(csv.DictReader(content))


def compile_workspace(refresh: bool) -> list[dict[str, Any]]:
    print("Compiling Workspace-Bench-Lite...")
    by_id = {row["absolute_id"]: row for row in load_workspace_rows()}
    records: list[dict[str, Any]] = []
    for directory, upstream_id, domain in WORKSPACE_TASKS:
        row = by_id[upstream_id]
        task_dir = TASKS_DIR / directory
        source_dir = task_dir / "source_docs"
        source_dir.mkdir(parents=True, exist_ok=True)
        data_manifest = parse_json_field(row["data_manifest"])
        for item in data_manifest:
            relative = f"task_lite_clean_en/{upstream_id}/{item['stored_relpath']}"
            encoded = urllib.parse.quote(relative, safe="/")
            download(
                f"{WORKSPACE_REPO}/resolve/main/{encoded}",
                source_dir / item["filename"],
                refresh,
            )
        deliverables = parse_json_field(row["output_files"])
        title = f"{row['persona']}: {domain.replace('-', ' ').title()}"
        write_prompt(task_dir / "prompt.md", title, row["task"], deliverables)
        rubric = {
            "rubrics": parse_json_field(row["rubrics"]),
            "rubric_types": parse_json_field(row["rubric_types"]),
            "file_dependency_graph": parse_json_field(row["file_dep_graph"]),
            "tested_capabilities": parse_json_field(row["tested_capabilities"]),
        }
        write_json(task_dir / "rubric.json", rubric)
        write_json(task_dir / "upstream_task.json", {key: parse_json_field(value) for key, value in row.items()})
        normalized = {
            "id": directory,
            "title": title,
            "domain": domain,
            "work_type": "workspace-analysis",
            "persona": row["persona"],
            "difficulty": row["task_diff"],
            "dataset": "Workspace-Bench-Lite",
            "upstream_id": upstream_id,
            "upstream_url": f"{WORKSPACE_REPO}?row={upstream_id}",
            "license": "MIT",
            "prompt": "prompt.md",
            "source_docs": "source_docs",
            "deliverables": deliverables,
            "rubric": "rubric.json",
        }
        write_json(task_dir / "task.json", normalized)
        records.append(normalized)
    return records


def clean_unselected_task_dirs(expected: set[str]) -> None:
    TASKS_DIR.mkdir(parents=True, exist_ok=True)
    for child in TASKS_DIR.iterdir():
        if child.is_dir() and child.name not in expected:
            shutil.rmtree(child)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_catalog(records: list[dict[str, Any]]) -> None:
    ordered = sorted(records, key=lambda record: record["id"])
    fields = [
        "id",
        "dataset",
        "domain",
        "title",
        "work_type",
        "upstream_id",
        "deliverables",
    ]
    with (ROOT / "catalog.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for record in ordered:
            row = {key: record.get(key, "") for key in fields}
            row["deliverables"] = ";".join(record["deliverables"])
            writer.writerow(row)
    write_json(ROOT / "catalog.json", ordered)


def write_coverage(records: list[dict[str, Any]]) -> None:
    lines = [
        "# Coverage matrix",
        "",
        "| # | Dataset | Domain | Task | Deliverables |",
        "|---:|---|---|---|---|",
    ]
    for index, record in enumerate(sorted(records, key=lambda item: item["id"]), start=1):
        outputs = ", ".join(f"`{item}`" for item in record["deliverables"])
        lines.append(
            f"| {index} | {record['dataset']} | {record['domain']} | "
            f"[{record['title']}](tasks/{record['id']}/prompt.md) | {outputs} |"
        )
    lines.extend(
        [
            "",
            "## Domain groups",
            "",
            "- Finance and strategy: commercial diligence, modeling, quantitative finance, tax, and global product strategy.",
            "- Legal: M&A, real estate, contracts, bankruptcy, litigation, and cross-border tax.",
            "- Operations: healthcare, logistics, emergency response, project controls, and sales operations.",
            "- Technical: materials engineering, systems architecture, data-heavy product analysis, and AI research.",
            "- Communication formats: memo, PDF, XLSX, PPTX, LaTeX, video/subtitles, operating manual, and research survey.",
            "",
        ]
    )
    (ROOT / "coverage.md").write_text("\n".join(lines), encoding="utf-8")


def write_source_manifest() -> None:
    MANIFESTS_DIR.mkdir(parents=True, exist_ok=True)
    paths: set[Path] = set()
    for task_dir in TASKS_DIR.iterdir():
        source = task_dir / "source_docs"
        if source.is_symlink():
            continue
        if source.is_dir():
            paths.update(path for path in source.rglob("*") if path.is_file())
    if SOURCE_POOLS_DIR.exists():
        paths.update(path for path in SOURCE_POOLS_DIR.rglob("*") if path.is_file())
    lines = [
        f"{sha256_file(path)}  {path.relative_to(ROOT).as_posix()}"
        for path in sorted(paths)
    ]
    (MANIFESTS_DIR / "source-files.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--refresh", action="store_true", help="Re-download existing upstream files")
    args = parser.parse_args()

    expected = {
        entry[0] for entry in AA_TASKS + GDP_TASKS + WORKSPACE_TASKS
    } | {entry["dir"] for entry in HARVEY_TASKS}
    clean_unselected_task_dirs(expected)
    SOURCE_POOLS_DIR.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    records.extend(compile_aa(args.refresh))
    records.extend(compile_harvey(args.refresh))
    records.extend(compile_gdpval(args.refresh))
    records.extend(compile_workspace(args.refresh))
    write_catalog(records)
    write_coverage(records)
    write_source_manifest()
    print(f"Compiled {len(records)} tasks into {ROOT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

