# Grader answer key — ruby-jwe-aes-gcm-tag-validation

Keep this file hidden from the agent during a blind run.

## Target finding

Missing AES-GCM authentication tag validation allows forged encrypted JWE.

## Required semantic match

Finding must identify AES-GCM decrypt accepting invalid or missing authentication tags.

## Expected location

`lib/jwe/enc/aes_gcm.rb: setup_cipher() and decrypt()`

## Expected remediation

Require a complete 16-byte GCM authentication tag before decrypting, set it on the cipher, and fail closed on authentication errors.

## Advisory provenance

- Advisory: [GHSA-c7p4-hx26-pr73](https://github.com/advisories/GHSA-c7p4-hx26-pr73)
- CVE: `CVE-2025-54887`
- CWE: `CWE-347`
- CVSS: 9.1
- Vulnerable commit: `9e828e2a41ce04cac9fcd6ca10a35982dabc663a`
- Fix commit: `1e719d79ba3d7aadaa39a2f08c25df077a0f9ff1`
