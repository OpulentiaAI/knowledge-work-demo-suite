#!/usr/bin/env python3
"""Validate the compiled suite using its real prompts and source documents."""

from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "tasks"
EXPECTED_DATASET_COUNTS = {
    "AA-Briefcase-Lite": 4,
    "Harvey Legal Agent Benchmark": 6,
    "OpenAI GDPval": 6,
    "Workspace-Bench-Lite": 4,
    "Synthetic Retail POS 2026 (Mendeley Data)": 3,
    "Daytona Windows OSWorld-Inspired Knowledge Work": 10,
    "UC Berkeley DataAgentBench": 7,
    "Tax Strategy Execution Manual-Inspired Advisory Work": 7,
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fail(message: str) -> None:
    raise AssertionError(message)


def main() -> int:
    task_dirs = sorted(path for path in TASKS_DIR.iterdir() if path.is_dir())
    if len(task_dirs) != 47:
        fail(f"Expected 47 task directories, found {len(task_dirs)}")

    ids: set[str] = set()
    datasets: Counter[str] = Counter()
    resolved_source_files: set[Path] = set()
    for task_dir in task_dirs:
        task_file = task_dir / "task.json"
        prompt_file = task_dir / "prompt.md"
        source_path = task_dir / "source_docs"
        if not task_file.is_file():
            fail(f"Missing {task_file}")
        if not prompt_file.is_file() or prompt_file.stat().st_size < 80:
            fail(f"Missing or undersized prompt: {prompt_file}")
        metadata = json.loads(task_file.read_text(encoding="utf-8"))
        for key in (
            "id",
            "title",
            "domain",
            "dataset",
            "upstream_id",
            "upstream_url",
            "license",
            "prompt",
            "source_docs",
            "deliverables",
            "rubric",
        ):
            if key not in metadata:
                fail(f"{task_file} lacks required key {key}")
        if metadata["id"] != task_dir.name:
            fail(f"Task ID mismatch in {task_file}")
        if metadata["id"] in ids:
            fail(f"Duplicate task ID {metadata['id']}")
        ids.add(metadata["id"])
        datasets[metadata["dataset"]] += 1
        if not str(metadata["upstream_url"]).startswith("https://"):
            fail(f"Invalid upstream URL in {task_file}")
        if not metadata["deliverables"] or not all(
            isinstance(item, str) and item.strip() for item in metadata["deliverables"]
        ):
            fail(f"No expected deliverables in {task_file}")
        if not source_path.is_dir():
            fail(f"Missing source_docs directory or resolvable symlink in {task_dir}")
        source_files = [path for path in source_path.rglob("*") if path.is_file()]
        if not source_files:
            fail(f"No source files for {task_dir.name}")
        for source_file in source_files:
            if source_file.stat().st_size == 0:
                fail(f"Empty source file: {source_file}")
            resolved_source_files.add(source_file.resolve())
        rubric_path = task_dir / metadata["rubric"]
        if not rubric_path.is_file() or rubric_path.stat().st_size == 0:
            fail(f"Missing rubric: {rubric_path}")
        if metadata["dataset"] == "Daytona Windows OSWorld-Inspired Knowledge Work":
            config_path = task_dir / metadata.get("daytona_windows_config", "")
            if not config_path.is_file():
                fail(f"Missing Daytona Windows config: {config_path}")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if config.get("os") != "windows":
                fail(f"Daytona task must target Windows: {config_path}")
            if config.get("output", {}).get("required_files") != metadata["deliverables"]:
                fail(f"Daytona output mismatch: {config_path}")
        if metadata["dataset"] == "UC Berkeley DataAgentBench":
            config_path = task_dir / metadata.get("dataagentbench_config", "")
            validator_path = task_dir / "validate.py"
            ground_truth_path = task_dir / "ground_truth.csv"
            if not config_path.is_file():
                fail(f"Missing DataAgentBench config: {config_path}")
            if not validator_path.is_file() or not ground_truth_path.is_file():
                fail(f"Missing DataAgentBench grader files: {task_dir}")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if config.get("read_only") is not True:
                fail(f"DataAgentBench task must be read-only: {config_path}")
            if config.get("answer_file") not in metadata["deliverables"]:
                fail(f"DataAgentBench output mismatch: {config_path}")
            if not (source_path / "db_config.yaml").is_file():
                fail(f"Missing DataAgentBench database config: {task_dir}")
            if not (source_path / "db_description.txt").is_file():
                fail(f"Missing DataAgentBench database description: {task_dir}")
            if not (source_path / "query_dataset").is_dir():
                fail(f"Missing DataAgentBench query dataset: {task_dir}")
        if metadata["dataset"] == "Tax Strategy Execution Manual-Inspired Advisory Work":
            config_path = task_dir / metadata.get("tax_strategy_config", "")
            if not config_path.is_file():
                fail(f"Missing tax strategy config: {config_path}")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if config.get("effective_tax_year") != 2026:
                fail(f"Tax strategy task must freeze the 2026 tax year: {config_path}")
            manual = config.get("manual_method_reference", {})
            if manual.get("confidential_manual_redistributed") is not False:
                fail(f"Confidential manual redistribution flag is unsafe: {config_path}")
            if config.get("output", {}).get("required_files") != metadata["deliverables"]:
                fail(f"Tax strategy output mismatch: {config_path}")
            if any(path.suffix.lower() == ".pdf" for path in source_files):
                fail(f"Tax strategy packet must not redistribute the confidential PDF: {task_dir}")
            required_sources = {
                "calculation_inputs.csv",
                "client_facts.md",
                "official_guidance.md",
            }
            if {path.name for path in source_files} != required_sources:
                fail(f"Tax strategy source packet mismatch: {task_dir}")
            answer_key_path = task_dir / "answer_key.md"
            if not answer_key_path.is_file() or answer_key_path.stat().st_size == 0:
                fail(f"Missing tax strategy answer key: {answer_key_path}")
            blind_run = config.get("blind_run", {})
            hidden = set(blind_run.get("grader_hidden", []))
            visible = set(blind_run.get("agent_visible", []))
            if not {"rubric.json", "answer_key.md"} <= hidden or hidden & visible:
                fail(f"Unsafe tax strategy blind-run isolation: {config_path}")
            rubric_data = json.loads(rubric_path.read_text(encoding="utf-8"))
            if sum(item.get("score", 0) for item in rubric_data) != 100:
                fail(f"Tax strategy rubric must total 100 points: {rubric_path}")

    if dict(datasets) != EXPECTED_DATASET_COUNTS:
        fail(f"Unexpected dataset balance: {dict(datasets)}")

    catalog_rows = list(csv.DictReader((ROOT / "catalog.csv").open(encoding="utf-8")))
    if len(catalog_rows) != 47:
        fail(f"Expected 47 catalog rows, found {len(catalog_rows)}")
    if {row["id"] for row in catalog_rows} != ids:
        fail("catalog.csv task IDs do not match task directories")

    manifest_path = ROOT / "manifests" / "source-files.sha256"
    manifest_entries: dict[Path, str] = {}
    for line in manifest_path.read_text(encoding="utf-8").splitlines():
        digest, relative = line.split("  ", 1)
        manifest_entries[(ROOT / relative).resolve()] = digest
    if set(manifest_entries) != resolved_source_files:
        missing = resolved_source_files - set(manifest_entries)
        extra = set(manifest_entries) - resolved_source_files
        fail(f"Manifest mismatch: missing={len(missing)} extra={len(extra)}")
    for path, expected_digest in manifest_entries.items():
        if sha256_file(path) != expected_digest:
            fail(f"SHA-256 mismatch: {path}")

    print(
        "PASS: 47 tasks, 8 datasets, "
        f"{len(resolved_source_files)} unique source files, all hashes verified"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
