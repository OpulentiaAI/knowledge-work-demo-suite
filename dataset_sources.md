# Dataset sources and selection rationale

## Benchmark class

This suite targets agentic knowledge work: tasks that require reading multiple
files, reconciling evidence, applying professional judgment, and producing a
work artifact such as a memo, model, workbook, presentation, report, or
operating manual.

## Anchor datasets

### AA-Briefcase-Lite

AA-Briefcase-Lite is the public example scenario for Artificial Analysis'
AA-Briefcase benchmark. The released scenario contains four related
commercial-diligence tasks using a shared workspace of reports, emails, Slack
exports, transcripts, spreadsheets, and company standards. It contributes the
suite's strongest long-horizon, cross-document, multimodal workflow.

Source: https://huggingface.co/datasets/ArtificialAnalysis/AA-Briefcase-Lite

### Harvey Legal Agent Benchmark

Harvey LAB packages legal assignments as instructions, synthetic matter
documents, expected deliverables, and pass/fail criteria. Six tasks were chosen
to span M&A diligence, real estate extraction, NDA playbook review, bankruptcy
drafting, litigation assessment, and cross-border tax structuring.

Requested source: https://github.com/OpulentiaAI/harvey-labs/tree/main/tasks

## Additional datasets

### OpenAI GDPval

GDPval contains 220 real-world tasks across 44 occupations. It is a close match
for this suite because each row provides a professional prompt, supporting
reference files, expected deliverable metadata, and a detailed rubric. The six
selected tasks extend coverage into quantitative finance, healthcare,
materials engineering, project management, sales, and cloud architecture.

Source: https://huggingface.co/datasets/openai/gdpval

### Workspace-Bench-Lite

Workspace-Bench evaluates agents on large, heterogeneous file workspaces and
explicit file-dependency graphs. Four English Lite tasks were selected for
product expense analysis, emergency operations, global product strategy, and
research synthesis. They add file traversal, cross-file aggregation, and
workspace learning without duplicating the legal and diligence domains.

Source: https://huggingface.co/datasets/Workspace-Bench/Workspace-Bench-Lite

## Considered but not selected

- WorkBench focuses on database state changes such as sending email and
  scheduling rather than document-grounded deliverables.
- Hedge-Bench is valuable but would over-weight finance in a 20-task set.
- Full Workspace-Bench is intentionally not vendored because its workspaces
  exceed 20 GB; the Lite source files named by the selected tasks are included.

