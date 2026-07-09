# Contributing to Casper TCG Oracle

Thanks for your interest! This repo is the Casper Network component of
[The Undesirables](https://the-undesirables.com) on-chain TCG price/risk oracle,
built for the Casper Agentic Buildathon.

## Getting Started

### Prerequisites
- [cargo-odra](https://github.com/odradev/cargo-odra)
- Rust toolchain `nightly-2026-01-01` (pinned in `rust-toolchain`)
- Python 3.11+
- `casper-client` CLI

### Build & Test
```bash
cargo test --lib          # run the contract unit tests (Odra mock backend)
cargo odra build -b casper # compile the WASM binary
```

## Making Changes

1. Fork and branch from `master`.
2. Keep the project **in a functional state at all times** — CI (`cargo fmt`,
   build, `cargo test --lib`) must pass.
3. Never commit secrets. `*.pem` and `.env` are `.gitignore`'d — keep it that way.
4. Open a PR against `master` with a clear description and, if on-chain behavior
   changes, a sample Testnet deploy hash.

## Reporting Issues

Use the issue templates. For **security** vulnerabilities, follow
[SECURITY.md](SECURITY.md) instead of opening a public issue.

## License

By contributing you agree your contributions are licensed under the
[Business Source License 1.1](LICENSE).
