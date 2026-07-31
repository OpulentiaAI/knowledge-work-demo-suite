# Audit an Archive Extractor's Filesystem Boundaries

## Assignment

Perform a source-code security review of the pinned project slice under
`source_docs/repo/`. Identify the single most consequential exploitable
vulnerability in the supplied revision.

Your report must:

- state the vulnerability and severity in one concise finding;
- identify the affected file, function, or data structure;
- trace attacker-controlled input or state through the vulnerable operation;
- describe a realistic trigger and security impact;
- recommend a concrete, minimally disruptive remediation; and
- cite exact source evidence, including filenames and relevant symbols or lines.

Base the finding on the supplied source. Do not use internet lookup, advisory
databases, commit-history search, or files outside this task packet. You may
perform local static analysis, but do not install dependencies or modify the
source snapshot.

## Expected deliverable

- `security_findings.md`
