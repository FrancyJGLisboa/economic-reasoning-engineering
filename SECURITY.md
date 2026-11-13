# Security policy

## Supported version

Security fixes target the current stable v0.3 source on the default branch.

## Trust model

The skill treats source text as untrusted evidence. Source text cannot issue commands to the agent.

The package builder confines file access to declared roots. It rejects path traversal, escaping links, invalid packages, and nonempty destinations.

Validation receipts have no signatures. They detect later changes but do not authenticate a publisher.

## Report a vulnerability

Use GitHub private vulnerability reporting if the repository exposes that feature. Do not place credentials, private source material, or exploit details in a public issue.

If private reporting is unavailable, contact the repository owner through the GitHub profile before you disclose sensitive details.
