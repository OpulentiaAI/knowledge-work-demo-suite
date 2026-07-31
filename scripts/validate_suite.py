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
    "Daytona Windows OSWorld-Inspired Knowledge Work": 11,
    "UC Berkeley DataAgentBench": 7,
    "Tax Strategy Execution Manual-Inspired Advisory Work": 7,
    "Devin Security Swarm Eval Fixtures": 5,
    "Mercor APEX-Accounting Dev Set": 5,
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
    if len(task_dirs) != 58:
        fail(f"Expected 58 task directories, found {len(task_dirs)}")

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
        if not any(path.stat().st_size > 0 for path in source_files):
            fail(f"No non-empty source material for {task_dir.name}")
        for source_file in source_files:
            if (
                source_file.stat().st_size == 0
                and metadata["dataset"] != "Devin Security Swarm Eval Fixtures"
            ):
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
        if metadata["dataset"] == "Devin Security Swarm Eval Fixtures":
            config_path = task_dir / metadata.get("security_eval_config", "")
            answer_key_path = task_dir / "answer_key.md"
            upstream_path = task_dir / "upstream_task.json"
            source_repo = source_path / "repo"
            source_manifest = source_path / "SOURCE_FILES.sha256"
            if not config_path.is_file():
                fail(f"Missing security eval config: {config_path}")
            if not answer_key_path.is_file() or not upstream_path.is_file():
                fail(f"Missing security grader metadata: {task_dir}")
            if not source_repo.is_dir() or not any(
                path.is_file() for path in source_repo.rglob("*")
            ):
                fail(f"Missing vulnerable source snapshot: {source_repo}")
            if not source_manifest.is_file():
                fail(f"Missing security source manifest: {source_manifest}")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if config.get("read_only") is not True or config.get("network") != "disabled":
                fail(f"Security eval must be read-only and offline: {config_path}")
            if config.get("answer_file") not in metadata["deliverables"]:
                fail(f"Security eval output mismatch: {config_path}")
            blind_run = config.get("blind_run", {})
            hidden = set(blind_run.get("grader_hidden", []))
            visible = set(blind_run.get("agent_visible", []))
            required_hidden = {"rubric.json", "answer_key.md", "upstream_task.json"}
            if not required_hidden <= hidden or hidden & visible:
                fail(f"Unsafe security blind-run isolation: {config_path}")
            rubric_data = json.loads(rubric_path.read_text(encoding="utf-8"))
            if sum(item.get("score", 0) for item in rubric_data) != 100:
                fail(f"Security eval rubric must total 100 points: {rubric_path}")
            upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
            if upstream.get("fixture_commit") != (
                "eeff76ad9232c1a2fc5ddfae453060b298dd53fd"
            ):
                fail(f"Unpinned security fixture provenance: {upstream_path}")
            snapshot = upstream.get("source_snapshot", {})
            repo_files = [path for path in source_repo.rglob("*") if path.is_file()]
            if snapshot.get("commit") != config.get("source_commit"):
                fail(f"Security source commit mismatch: {task_dir}")
            if snapshot.get("file_count") != len(repo_files):
                fail(f"Security source file-count mismatch: {task_dir}")
            for license_file in snapshot.get("license_files", []):
                if not (source_repo / license_file).is_file():
                    fail(f"Missing preserved upstream license: {source_repo / license_file}")
            packet_hashes: dict[Path, str] = {}
            for line in source_manifest.read_text(encoding="utf-8").splitlines():
                digest, relative = line.split("  ", 1)
                packet_hashes[source_path / relative] = digest
            expected_packet_files = {
                path
                for path in source_path.rglob("*")
                if path.is_file() and path != source_manifest
            }
            if set(packet_hashes) != expected_packet_files:
                fail(f"Security packet hash inventory mismatch: {source_manifest}")
            for path, expected_digest in packet_hashes.items():
                if sha256_file(path) != expected_digest:
                    fail(f"Security packet SHA-256 mismatch: {path}")
            visible_contract = "\n".join(
                [
                    prompt_file.read_text(encoding="utf-8"),
                    task_file.read_text(encoding="utf-8"),
                    config_path.read_text(encoding="utf-8"),
                    (source_path / "UPSTREAM_SOURCE.md").read_text(encoding="utf-8"),
                ]
            )
            for secret in (
                upstream.get("ghsa"),
                upstream.get("cve"),
                upstream.get("target"),
                upstream.get("match_rule"),
                upstream.get("fix_commit"),
            ):
                if secret and str(secret) in visible_contract:
                    fail(f"Security answer leakage in agent-visible contract: {task_dir}")
        if metadata["dataset"] == "Mercor APEX-Accounting Dev Set":
            config_path = task_dir / metadata.get("apex_accounting_config", "")
            answer_key_path = task_dir / "answer_key.md"
            upstream_path = task_dir / "upstream_task.json"
            source_manifest = source_path / "SOURCE_FILES.sha256"
            if not config_path.is_file():
                fail(f"Missing APEX-Accounting config: {config_path}")
            if not answer_key_path.is_file() or not upstream_path.is_file():
                fail(f"Missing APEX-Accounting grader metadata: {task_dir}")
            if not source_manifest.is_file():
                fail(f"Missing APEX-Accounting source manifest: {source_manifest}")
            if not (source_path / "UPSTREAM_LICENSE").is_file():
                fail(f"Missing APEX-Accounting CC BY license: {source_path}")
            config = json.loads(config_path.read_text(encoding="utf-8"))
            if config.get("dataset_commit") != (
                "bf5e8c99117b7ee763d79ad2c64563ac844d77d2"
            ):
                fail(f"Unpinned APEX-Accounting dataset revision: {config_path}")
            if config.get("read_only") is not True or config.get("network") != "disabled":
                fail(f"APEX-Accounting task must be read-only and offline: {config_path}")
            if config.get("answer_file") not in metadata["deliverables"]:
                fail(f"APEX-Accounting output mismatch: {config_path}")
            if config.get("output", {}).get("required_files") != metadata["deliverables"]:
                fail(f"APEX-Accounting required-files mismatch: {config_path}")
            blind_run = config.get("blind_run", {})
            hidden = set(blind_run.get("grader_hidden", []))
            visible = set(blind_run.get("agent_visible", []))
            required_hidden = {"rubric.json", "answer_key.md", "upstream_task.json"}
            if not required_hidden <= hidden or hidden & visible:
                fail(f"Unsafe APEX-Accounting blind-run isolation: {config_path}")
            upstream = json.loads(upstream_path.read_text(encoding="utf-8"))
            rubric_data = json.loads(rubric_path.read_text(encoding="utf-8"))
            if not rubric_data or rubric_data != upstream.get("rubric"):
                fail(f"APEX-Accounting rubric differs from upstream: {rubric_path}")
            if upstream.get("gold_output", "").strip() not in answer_key_path.read_text(
                encoding="utf-8"
            ):
                fail(f"APEX-Accounting answer key differs from upstream: {answer_key_path}")
            if upstream.get("metadata", {}).get("output_type") != "console_text":
                fail(f"Unexpected APEX-Accounting output type: {upstream_path}")
            if upstream.get("prompt", "").strip() not in prompt_file.read_text(
                encoding="utf-8"
            ):
                fail(f"APEX-Accounting prompt differs from upstream: {prompt_file}")
            support_files = {
                "SOURCE_FILES.sha256",
                "SOURCE_PROVENANCE.md",
                "UPSTREAM_LICENSE",
            }
            actual_context = {
                path.name for path in source_files if path.name not in support_files
            }
            if actual_context != set(upstream.get("context_files", [])):
                fail(f"APEX-Accounting context-file mismatch: {task_dir}")
            packet_hashes: dict[Path, str] = {}
            for line in source_manifest.read_text(encoding="utf-8").splitlines():
                digest, relative = line.split("  ", 1)
                packet_hashes[source_path / relative] = digest
            expected_packet_files = {
                path
                for path in source_path.iterdir()
                if path.is_file() and path != source_manifest
            }
            if set(packet_hashes) != expected_packet_files:
                fail(f"APEX-Accounting packet hash inventory mismatch: {source_manifest}")
            for path, expected_digest in packet_hashes.items():
                if sha256_file(path) != expected_digest:
                    fail(f"APEX-Accounting packet SHA-256 mismatch: {path}")
            visible_contract = "\n".join(
                [
                    prompt_file.read_text(encoding="utf-8"),
                    task_file.read_text(encoding="utf-8"),
                    config_path.read_text(encoding="utf-8"),
                    (source_path / "SOURCE_PROVENANCE.md").read_text(encoding="utf-8"),
                ]
            )
            if upstream.get("gold_output", "").strip() in visible_contract:
                fail(f"APEX-Accounting gold-output leakage: {task_dir}")
            for criterion in rubric_data:
                description = criterion.get("description", "").strip()
                if description and description in visible_contract:
                    fail(f"APEX-Accounting rubric leakage: {task_dir}")

    if dict(datasets) != EXPECTED_DATASET_COUNTS:
        fail(f"Unexpected dataset balance: {dict(datasets)}")

    catalog_rows = list(csv.DictReader((ROOT / "catalog.csv").open(encoding="utf-8")))
    if len(catalog_rows) != 58:
        fail(f"Expected 58 catalog rows, found {len(catalog_rows)}")
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
        "PASS: 58 tasks, 10 datasets, "
        f"{len(resolved_source_files)} unique source files, all hashes verified"
    )
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except AssertionError as error:
        print(f"FAIL: {error}", file=sys.stderr)
        raise SystemExit(1)
