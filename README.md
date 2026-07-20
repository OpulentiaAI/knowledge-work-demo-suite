# Knowledge Work Demo Suite

A compact, source-grounded collection of 20 professional knowledge-work tasks
compiled from four public benchmarks. Every task contains:

- `prompt.md` — a standalone assignment for an agent or model;
- `task.json` — normalized metadata, provenance, inputs, and expected outputs;
- `source_docs/` — the real upstream working files, or a symlink to a shared
  source pool where several tasks use the same workspace;
- `rubric.json` or `rubric.jsonl` — upstream evaluation criteria when released.

The suite favors realistic deliverables over short-answer questions. It covers
commercial due diligence, financial modeling, legal drafting and review,
healthcare operations, industrial engineering, project management, sales,
systems architecture, product analysis, logistics, research, and global
operations.

## Quick start

Inspect the catalog:

```bash
python3 scripts/validate_suite.py
column -s, -t < catalog.csv | less -S
```

Run a task by giving an agent the contents of `prompt.md`, read access to its
`source_docs/`, and a writable output directory. Expected output filenames are
listed in `task.json`.

Rebuild or refresh the suite from the live upstream datasets:

```bash
python3 scripts/compile_suite.py
python3 scripts/compile_suite.py --refresh
```

The compiler uses only the Python standard library. Downloads are resumable:
non-empty local files are reused unless `--refresh` is passed.

## Layout

```text
tasks/
  001-aa-market-overview/
    prompt.md
    task.json
    rubric.jsonl
    source_docs -> ../../source_pools/aa-briefcase-lite
source_pools/
  aa-briefcase-lite/
catalog.csv
coverage.md
dataset_sources.md
manifests/source-files.sha256
scripts/
```

## Selection

| Dataset | Tasks | Role in this suite |
|---|---:|---|
| AA-Briefcase-Lite | 4 | Long-horizon commercial diligence and multimodal executive output |
| Harvey Legal Agent Benchmark | 6 | Legal analysis, review, drafting, transactions, disputes, and tax |
| OpenAI GDPval | 6 | Cross-industry professional artifacts in finance, healthcare, engineering, project delivery, sales, and IT |
| Workspace-Bench-Lite | 4 | File-heavy product, logistics, operations, and research work |

The collection is a curated demo set, not a replacement for any upstream
benchmark and not suitable for reporting upstream leaderboard scores.

## Data and licensing

The repository-level MIT license applies only to original scripts and
documentation. Upstream materials remain governed by their source licenses or
terms. In particular, the GDPval dataset card does not declare a standard
license, so GDPval-derived materials are marked `upstream terms apply`.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[dataset_sources.md](dataset_sources.md).

