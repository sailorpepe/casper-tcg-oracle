# Security Policy

## Reporting a Vulnerability

The Casper TCG Oracle handles on-chain price commitments and payment-gated API
access. We take security seriously.

**Please do not open public issues for security vulnerabilities.**

Instead, report privately to:

- **Email:** sailorpepe@the-undesirables.com
- **Subject:** `SECURITY — casper-tcg-oracle`

Please include:
- A description of the issue and its impact
- Steps to reproduce (proof-of-concept if possible)
- Any suggested remediation

We aim to acknowledge reports within **72 hours** and to provide a remediation
timeline after triage. Responsible disclosure is appreciated — we will credit
reporters who wish to be named once a fix is released.

## Scope

In scope:
- The Odra/Rust smart contract (`src/merkle_oracle.rs`)
- The deployment and Merkle-builder tooling (`casper_*.py`)
- The Casper x402 payment-gate integration

Out of scope:
- Testnet-only funds (this project targets Casper **Testnet**)
- Third-party dependencies (report upstream; we track via Dependabot)

## Key Handling

Deployment keys (`*.pem`) are **never** committed — they are `.gitignore`'d by
construction. Never paste a private key into an issue, PR, or log.
