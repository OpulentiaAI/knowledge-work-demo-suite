# Third-party notices

This repository contains selected prompts, rubrics, and source documents from
third-party datasets. Those materials are not relicensed by the repository's
MIT license.

## AA-Briefcase-Lite

- Publisher: Artificial Analysis
- Source: https://huggingface.co/datasets/ArtificialAnalysis/AA-Briefcase-Lite
- Upstream license: Apache License 2.0
- Included: four public week-one task prompts, task-specific checks, and the
  released shared/week source workspace.

## Harvey Legal Agent Benchmark (LAB)

- Publisher: Harvey AI
- Requested source fork: https://github.com/OpulentiaAI/harvey-labs
- Canonical upstream: https://github.com/harveyai/harvey-labs
- Upstream license: MIT
- Included: six task definitions, criteria, and their synthetic matter files.

## OpenAI GDPval

- Publisher: OpenAI
- Source: https://huggingface.co/datasets/openai/gdpval
- Upstream terms: the dataset card did not declare a standardized license when
  this suite was compiled on 2026-07-20. Use and redistribution remain subject
  to the upstream dataset terms and disclosures.
- Included: six prompts, rubrics, and reference files. Expert deliverables are
  intentionally excluded to prevent answer leakage.

## Workspace-Bench-Lite

- Publisher: OpenDataBox / Workspace-Bench
- Source: https://huggingface.co/datasets/Workspace-Bench/Workspace-Bench-Lite
- Code and benchmark license: MIT
- Included: four task rows, rubrics, dependency metadata, and the exact files
  named by each task's data manifest.

## Daytona Windows OSWorld-Inspired Knowledge Work

- Method reference: https://www.daytona.io/dotfiles/osworld-on-daytona-windows-sandboxes
- Included: eleven original task definitions, synthetic local evidence packets,
  Daytona Windows runtime contracts, and original evaluation rubrics.
- Not included: OSWorld Windows task files, Daytona source code, Office
  software, private credentials, live-web task state, or the user-provided
  screenshot used as the private design reference for task `048`.

## UC Berkeley DataAgentBench

- Publisher: UC Berkeley EPIC
- Source: https://github.com/ucbepic/DataAgentBench
- Data mirror: https://huggingface.co/datasets/ruiyingm/DataAgentBench-data
- Upstream terms: the repository did not declare a repository-wide license
  when these packets were compiled on 2026-07-26. Use and redistribution
  remain subject to the upstream project and source-dataset terms.
- Included: seven query prompts, official validators and ground-truth files,
  database descriptions and configurations, and the bounded database files
  required by those queries.

## Tax Strategy Execution Manual-Inspired Advisory Work

- Private method reference: `Tax Strategy Execution Manual`, July 2026.
- Not included: the confidential manual, page images, extracted text, or
  quotations from it.
- Included: seven original task definitions, synthetic client fact packets,
  calculation inputs, evaluation rubrics, links to official United States
  government guidance, and a dated factual extract of five publicly listed
  Chicago meeting-space asking rates for task `046`.
- Not included: copies, screenshots, images, or descriptive text from the
  Peerspace or workin.space listing pages. Listing names, locations, capacity,
  rates, retrieval date, and source URLs are preserved as factual provenance.
- United States government works and linked guidance are not relicensed by
  this repository. The original task text and synthetic fixtures are covered
  by the repository MIT license.

## Devin Security Swarm Eval Fixtures

- Fixture publisher: r2d4
- Source:
  https://github.com/r2d4/devin-security-evals/tree/eeff76ad9232c1a2fc5ddfae453060b298dd53fd
- Fixture-repository terms: no repository-wide license was declared when the
  five packets were compiled on 2026-07-31. The normalized prompts, run
  contracts, and rubrics in this repository are original adaptations; fixture
  facts and identifiers remain subject to upstream terms.
- Included source snapshots and licenses:
  - `aws/amazon-redshift-python-driver` — Apache License 2.0; `LICENSE` and
    `NOTICE` preserved.
  - `harttle/liquidjs` — MIT License; `LICENSE` preserved.
  - `ibireme/yyjson` — MIT License; `LICENSE` preserved.
  - `brendan-duncan/archive` — MIT License; `LICENSE` preserved.
  - `jwt/ruby-jwe` — MIT License; `LICENSE.md` preserved.
- Included: five bounded source slices from exact vulnerable commits, source
  provenance and hashes, original blind prompts, grader-only semantic answer
  keys, and normalized metadata.
- Not included: full repository histories, fixed source revisions, complete
  upstream test suites, or unrelated files from the five source projects.

## Mercor APEX-Accounting Dev Set

- Publishers: Mercor and Ramp
- Source:
  https://huggingface.co/datasets/mercor/apex-accounting/tree/bf5e8c99117b7ee763d79ad2c64563ac844d77d2
- License: Creative Commons Attribution 4.0 International
- Included: five public development-set prompts, binary rubric criteria,
  expert answers, task metadata, and the exact task-required accounting
  workbooks, exports, PDFs, text files, and Word documents.
- Adaptation: upstream console responses are normalized to an `answer.txt`
  deliverable; source files are flattened to match the runtime layout
  documented by the publisher.
- Not included: the closed 160-task scored benchmark, unreleased worlds,
  Mercor's internal grading template, or the unshipped accounting-software
  interface used in official runs.
- Results from these five public development tasks are not official
  APEX-Accounting leaderboard scores.

Third-party trademarks and names are used only to identify provenance.
