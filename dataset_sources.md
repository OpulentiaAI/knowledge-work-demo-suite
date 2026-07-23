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

### Synthetic Retail POS 2026 (Mendeley Data)

The Synthetic Multi-Store Retail Point-of-Sale Transaction Dataset in Square
POS Export Format is a public CC BY 4.0, 2026-released synthetic dataset with
transaction line items, store and category fields, prices, discounts, refunds,
costs, profit, and a documented event-generation model. Three original tasks
derive small, agent-facing sales packets from the public export. The benchmark
asks an agent to diagnose why sales increased or declined, quantify the
observed drivers, distinguish evidence from inference, and recommend a
measurable response. The packets exclude generator multipliers and other
answer-key parameters.

Source: https://data.mendeley.com/datasets/39xdjxgnmf/1

### Daytona Windows OSWorld-Inspired Knowledge Work

These ten original task packets adapt the execution pattern described in
Daytona's Windows OSWorld article to the team's Daytona sandbox runtime. They
cover two Excel, two Word, two PowerPoint, and four Outlook-plus-Office
multi-app workflows. Each task stages only synthetic, local evidence; declares
the required Office apps and output path; starts from a resettable Windows
snapshot; restricts the agent to visible mouse/keyboard interaction; and uses
post-run artifact inspection. This makes the tasks suitable for deterministic
Daytona Windows evaluation without reproducing OSWorld data or requiring
private OAuth credentials or live web state.

Method source: https://www.daytona.io/dotfiles/osworld-on-daytona-windows-sandboxes

## Considered but not selected

- WorkBench focuses on database state changes such as sending email and
  scheduling rather than document-grounded deliverables.
- Hedge-Bench is valuable but would over-weight finance in a 20-task set.
- Full Workspace-Bench is intentionally not vendored because its workspaces
  exceed 20 GB; the Lite source files named by the selected tasks are included.
- OSWorld Windows task data is not vendored or represented as part of this
  collection; the Daytona article is used solely as a public method reference.
