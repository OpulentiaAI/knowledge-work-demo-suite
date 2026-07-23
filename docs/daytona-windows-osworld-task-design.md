# Daytona Windows Office Task Design

These ten task packets are original office-suite and multi-application
workflows designed for the team's Daytona Windows sandbox runtime. They take
their operating pattern from Daytona's OSWorld write-up, not its task files:
one natural-language instruction is shown to the agent; a known snapshot
stages the workspace; the agent works through visible desktop interaction; and
the runner inspects only the final artifacts.

## Runtime contract

- Start every attempt from the `daytona-windows-office-v1` snapshot, with the
  Office applications required by the selected task installed.
- Restage `source_docs/` to the path declared in `daytona_windows.json` before
  the first screenshot. Write deliverables only to the declared output path.
- Use a strict visible-UI policy: `pyautogui` and `time` are permitted; shell,
  direct filesystem APIs, network, and package installation are blocked.
- Keep the sandbox offline after snapshot creation. All evidence is bundled in
  the task workspace, so no account, OAuth credential, live website, or
  changing external result is necessary.
- Score after the agent stops by inspecting the named Office artifacts against
  `rubric.json` and the declarative checks in `daytona_windows.json`.

## Task families

| IDs | Family | Apps | Evaluation surface |
|---|---|---|---|
| 024-025 | Excel | Excel | sheets, formulas, calculated values, chart presence |
| 026-027 | Word | Word | document text, sections, tables, business-format requirements |
| 028-029 | PowerPoint | PowerPoint | slide count, titles, chart/table content, required decisions/checklists |
| 030-033 | Multi-app | Outlook plus Word/Excel or PowerPoint | reconciled facts and cross-artifact deliverables |

The format deliberately avoids the two fragile classes called out in the
Daytona article: private OAuth-bound tasks and live website tasks. The JSON is
a runner-agnostic Daytona contract rather than a claim that it is an exact
OSWorld schema. An adapter may translate it to the runner's task/setup/evaluator
interfaces.

Method source: <https://www.daytona.io/dotfiles/osworld-on-daytona-windows-sandboxes>
