# Knowledge Work Demo Suite

A compact, source-grounded collection of 47 professional knowledge-work tasks
compiled from eight benchmark families and task-design references. Every task contains:

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

The validator should report 47 tasks, eight datasets, and verified hashes for
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
| Synthetic Retail POS 2026 (Mendeley Data) | 3 | Evidence-based retail sales diagnosis with deterministic source packets |
| Daytona Windows OSWorld-Inspired Knowledge Work | 10 | Original, snapshot-ready Office and multi-app workflows for strict visible-UI Daytona Windows sandbox runs |
| UC Berkeley DataAgentBench | 7 | Cross-database analysis across publishing, civic projects, CRM policy, local markets, music revenue, procurement, and investments |
| Tax Strategy Execution Manual-Inspired Advisory Work | 7 | Execution-focused education, retirement, family-payroll, home-rental, and health-savings planning using synthetic facts and official federal guidance |

The collection is a curated demo set, not a replacement for any upstream
benchmark and not suitable for reporting upstream leaderboard scores.

## Daytona Windows Office tasks

Tasks `024` through `033` are tailored to a Daytona Windows sandbox runtime.
They use staged, offline synthetic evidence; resettable app state; and
post-run inspection of native Office artifacts. The packet configuration
enforces a visible-UI-only agent policy and names the required snapshot apps,
workspace path, output path, and evaluator checks. See
[the Daytona/OSWorld task design](docs/daytona-windows-osworld-task-design.md)
for the run contract and task-family breakdown.

## DataAgentBench tasks

Tasks `034` through `040` preserve seven DataAgentBench queries and the exact
database files needed to answer each one. Their `source_docs/` directories
contain the upstream database description, database configuration, and
read-only SQLite, DuckDB, PostgreSQL dump, or MongoDB BSON inputs. No live
database is required if the runner can inspect those formats directly; an
official-harness-compatible runner can instead load them using
`source_docs/db_config.yaml`.

Each task produces one plain-text deliverable:

```bash
TASK=036-dab-crm-quote-policy
WORKSPACE="$(pwd)/runs/$TASK/workspace"
rm -rf "$WORKSPACE"
mkdir -p "$WORKSPACE" "runs/$TASK/output"
cp "tasks/$TASK/prompt.md" "tasks/$TASK/task.json" \
  "tasks/$TASK/dataagentbench.json" "$WORKSPACE/"
ln -s "$(pwd)/tasks/$TASK/source_docs" "$WORKSPACE/source_docs"
```

Give only `$WORKSPACE` to the agent. This stages the prompt, normalized
contract, runtime metadata, and source databases without exposing the grader.
After the agent writes `runs/$TASK/output/answer.txt`, score it from the
repository root:

```bash
python3 - "tasks/$TASK" "runs/$TASK/output/answer.txt" <<'PY'
import importlib.util
import pathlib
import sys

task_dir = pathlib.Path(sys.argv[1])
answer = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8")
spec = importlib.util.spec_from_file_location("dab_validator", task_dir / "validate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
passed, reason = module.validate(answer)
print("PASS" if passed else "FAIL", reason)
raise SystemExit(0 if passed else 1)
PY
```

The included grader files are for transparent local evaluation. Do not expose
`ground_truth.csv`, `validate.py`, or `rubric.json` to the agent during a
blind run.

## Tax strategy execution tasks

Tasks `041` through `047` cover a 529 plan, a solo 401(k), a small-employer
401(k), employing an owner's child, employing an owner's spouse, a section
280A(g) home-rental arrangement, and HSA eligibility and funding.

The public packets contain original synthetic client facts and links to
official IRS, Department of Labor, and U.S. Code guidance. The user-supplied
`Tax Strategy Execution Manual` informed the execution-oriented task structure,
but the confidential PDF is not included or quoted. Each answer contract is
frozen to federal tax year 2026 and requires an advisory memo plus a
formula-driven workbook.

For a blind run, expose only the files listed in `tax_strategy.json`. Keep
`rubric.json` and `answer_key.md` away from the agent, then use both to review
the submitted memo and workbook.

## Data and licensing

The repository-level MIT license applies only to original scripts and
documentation. Upstream materials remain governed by their source licenses or
terms. In particular, the GDPval dataset card does not declare a standard
license, so GDPval-derived materials are marked `upstream terms apply`.
See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) and
[dataset_sources.md](dataset_sources.md).
