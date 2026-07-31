# Grader answer key — archive-path-traversal

Keep this file hidden from the agent during a blind run.

## Target finding

Symlink entries let archive extraction write files outside the target directory.

## Required semantic match

Finding must identify symlink-based archive extraction writing outside the intended destination.

## Expected location

`lib/src/io/extract_archive_to_disk.dart`

## Expected remediation

Reject absolute or escaping symlink targets and verify the normalized resolved link destination remains within the extraction root.

## Advisory provenance

- Advisory: [GHSA-9v85-q87q-g4vg](https://github.com/advisories/GHSA-9v85-q87q-g4vg)
- CVE: `CVE-2023-39139`
- CWE: `CWE-22`
- CVSS: 7.8
- Vulnerable commit: `85ac8df7f8e800abe3bb1343cae596c82de8802c`
- Fix commit: `6de492385d72af044231c4163dff13a43d991c83`
