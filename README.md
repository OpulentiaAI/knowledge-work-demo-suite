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

Clone the suite and validate the downloaded task workspaces:

```bash
git clone https://github.com/OpulentiaAI/knowledge-work-demo-suite.git
cd knowledge-work-demo-suite
python3 scripts/validate_suite.py
```

The validator should report 20 tasks, four datasets, and verified hashes for
all source files.

## Run one use case

Each directory directly under `tasks/` is an independent use case. The
repository packages the task and rubric but does not require a specific model,
agent CLI, or evaluation harness.

### 1. Choose a task

Browse [coverage.md](coverage.md) for a human-readable matrix or inspect the
CSV catalog:

```bash
python3 - <<'PY'
import csv

for row in csv.DictReader(open("catalog.csv", encoding="utf-8")):
    print(f"{row['id']:45} {row['domain']:28} {row['title']}")
PY
```

For example:

```bash
TASK=012-gdpval-materials-lab
```

### 2. Inspect its run contract

```bash
sed -n '1,240p' "tasks/$TASK/prompt.md"
python3 -m json.tool "tasks/$TASK/task.json"
find -L "tasks/$TASK/source_docs" -type f | sort
```

The normalized `task.json` declares:

- the upstream dataset and task ID;
- the professional domain and work type;
- the source-document directory;
- the exact required deliverable filename or filenames;
- the rubric file used to review the result.

### 3. Create an output directory

Keep generated work outside the immutable task workspace:

```bash
OUTPUT_DIR="$(pwd)/runs/$TASK/output"
mkdir -p "$OUTPUT_DIR"
```

`runs/` is ignored by Git.

### 4. Give the task to an agent

Open `tasks/$TASK/` as the agent's working directory. Give the agent this
instruction, substituting the absolute output path printed below:

```bash
printf 'Task workspace: %s\nOutput directory: %s\n' \
  "$(pwd)/tasks/$TASK" "$OUTPUT_DIR"
```

```text
Complete the assignment in prompt.md. Read all relevant files under
source_docs/ and treat them as the authoritative workspace. Write every
required deliverable, using the exact filenames declared in task.json, to
<OUTPUT_DIR>. Do not modify prompt.md, task.json, rubric files, or source_docs.
```

This contract works with Codex, Claude Code, or another file-capable agent.
The agent needs read access to the selected task directory and write access
only to the output directory.

### 5. Check the outputs

List the required filenames:

```bash
python3 - "$TASK" <<'PY'
import json
import pathlib
import sys

task = json.loads(
    (pathlib.Path("tasks") / sys.argv[1] / "task.json").read_text()
)
for filename in task["deliverables"]:
    print(filename)
PY
```

Confirm those files exist and are non-empty under `runs/$TASK/output/`, then
review the work against `rubric.json` or `rubric.jsonl` in the task directory.
Rubrics are preserved from upstream; this repository does not claim that
scores produced by a different agent harness are comparable to official
leaderboard scores.

### Example task workspace

```text
tasks/012-gdpval-materials-lab/
├── prompt.md
├── task.json
├── rubric.json
├── upstream_task.json
└── source_docs/
    ├── Data.xlsx
    └── Work Request MATL LAB.pdf
```

The expected output for this example is
`runs/012-gdpval-materials-lab/output/Results Memo v2.pdf`.

## Refresh the source collection

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
