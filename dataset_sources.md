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

These eleven original task packets adapt the execution pattern described in
Daytona's Windows OSWorld article to the team's Daytona sandbox runtime. They
cover three Excel, two Word, two PowerPoint, and four Outlook-plus-Office
multi-app workflows. The third Excel case preserves the workbook requirements
from a user-provided screenshot while replacing the unseen source data with an
original three-scenario crew and hourly-volume workbook. Each task stages only
synthetic, local evidence; declares
the required Office apps and output path; starts from a resettable Windows
snapshot; restricts the agent to visible mouse/keyboard interaction; and uses
post-run artifact inspection. This makes the tasks suitable for deterministic
Daytona Windows evaluation without reproducing OSWorld data or requiring
private OAuth credentials or live web state.

Method source: https://www.daytona.io/dotfiles/osworld-on-daytona-windows-sandboxes

### UC Berkeley DataAgentBench

DataAgentBench evaluates agents on realistic questions that require joining,
normalizing, and interpreting information across heterogeneous databases. The
seven selected queries cover publishing analytics, civic project funding, CRM
quote compliance, local-business research, music revenue, federal procurement,
and long-run index performance. Each packet includes only the databases needed
for that query, the upstream schema description and connection configuration,
and the official transparent validator.

Source: https://github.com/ucbepic/DataAgentBench

### Tax Strategy Execution Manual-Inspired Advisory Work

Seven original task packets translate an execution-oriented tax-advisory
method into deterministic cases covering a 529 plan, solo and employer 401(k)
plans, wages paid to an owner's child and spouse, a section 280A(g) home-rental
arrangement, and HSA planning. Client names, taxpayer facts, and output
contracts are synthetic. Task `046` adds five dated Chicago meeting-space
asking-rate observations derived from linked public listings so that its
market-rate analysis is location-specific and auditable. The listing pages are
not copied, the asking rates are not represented as completed transactions,
and the task requires refreshed quotes before real-world use. The cases freeze
their federal-law assumptions to 2026 and cite current IRS, Department of
Labor, and U.S. Code sources inside each packet.

The user-supplied `Tax Strategy Execution Manual` (July 2026) was used only as
a private method reference for workflow structure, execution controls, and
review emphasis. Because the manual is marked confidential and for internal
use, the PDF and its text are not redistributed in this public repository.

Primary public sources:

- https://www.irs.gov/
- https://www.dol.gov/agencies/ebsa
- https://uscode.house.gov/
- https://www.peerspace.com/pages/listings/57a0c3d8abe58d09009f4ca2
- https://book.workin.space/en/united-states/chicago/meeting-room

### Devin Security Swarm Eval Fixtures

The public `r2d4/devin-security-evals` repository reconstructs 34 security
fixtures around real published vulnerabilities and pins a vulnerable and fixed
commit for each case. Five fixtures were selected to span Python, JavaScript,
C, Dart, and Ruby, as well as code injection, prototype inheritance, memory
safety, filesystem traversal, and cryptographic authentication.

This suite converts those fixture definitions into blind, offline source-code
audits. Each packet contains a generic audit prompt plus a bounded, byte-exact
source slice from the named vulnerable commit. Advisory identifiers, fixed
commits, target descriptions, semantic match rules, rubrics, and answer keys
remain grader-only. The source snapshot records every included path and
preserves the original project's license file.

Fixture source:
https://github.com/r2d4/devin-security-evals/tree/eeff76ad9232c1a2fc5ddfae453060b298dd53fd

Pinned source repositories:

- https://github.com/aws/amazon-redshift-python-driver
- https://github.com/harttle/liquidjs
- https://github.com/ibireme/yyjson
- https://github.com/brendan-duncan/archive
- https://github.com/jwt/ruby-jwe

## Considered but not selected

- WorkBench focuses on database state changes such as sending email and
  scheduling rather than document-grounded deliverables.
- Hedge-Bench is valuable but would over-weight finance in a 20-task set.
- Full Workspace-Bench is intentionally not vendored because its workspaces
  exceed 20 GB; the Lite source files named by the selected tasks are included.
- OSWorld Windows task data is not vendored or represented as part of this
  collection; the Daytona article is used solely as a public method reference.
- The private screenshot used to specify task `048` is not vendored; only its
  workbook requirements and SHA-256 provenance are preserved.
- The full DataAgentBench corpus contains much larger datasets and more query
  families; only seven bounded, independently runnable cases are included.
- The confidential Tax Strategy Execution Manual is not vendored; its seven
  cases use original fixtures and public government guidance.
