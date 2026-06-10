<div align="center">

<img src="https://raw.githubusercontent.com/sailorpepe/undesirables-x402-server/main/assets/banner.png" alt="TCG Oracle Banner" width="100%" />

# ⛓️ Casper TCG Oracle (Merkle Price Oracle)

**Agentic Buildathon Phase 1 & 2 • Odra WASM Smart Contracts • Python Deployment Proxy**

![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![Casper Network](https://img.shields.io/badge/Chain-Casper_Testnet-FF0000?style=flat-square&logo=casper&logoColor=white)
![Odra](https://img.shields.io/badge/Framework-Odra-blue?style=flat-square)
![License: BSL-1.1](https://img.shields.io/badge/License-BSL_1.1-red?style=flat-square)

[Contract Explorer (Testnet)](https://testnet.cspr.cloud/contract/hash-5e160e1d845e2c438343ab6a084620b7bc603099cd3ba3f938c4b1b88e17b8f9) · [x402 Server Integration](https://github.com/sailorpepe/undesirables-x402-server)

</div>

---

## ⚡ Overview

This repository houses the **Merkle Price Oracle** for the **Casper Testnet**, built as part of the Agentic Buildathon. It provides trustless, on-chain verification for over 276,000 Trading Card Game (TCG) products and connects directly to the [LitVM x402 Server ecosystem](https://github.com/sailorpepe/undesirables-x402-server).

By porting our core EVM Solidity pricing logic into **Odra / Rust WebAssembly**, we bring institutional-grade stochastic finance modeling (Merton Jump-Diffusion Monte Carlo) to the Casper Network.

---

## 🏗️ Architecture

### 1. Smart Contract (Rust / Odra)
- **`src/merkle_oracle.rs`**: Core price verification logic. Takes a Merkle root and allows verification of TCG price proofs directly on the Casper network.
- **WASM Build**: Compiled down to a secure `MerklePriceOracle.wasm` binary using `cargo odra build`.

### 2. Secure Deployment Proxy
- **`casper_proxy.py`**: A custom HTTP middleware proxy that safely routes local JSON-RPC requests to `node.testnet.cspr.cloud/rpc`, seamlessly injecting CSPR API authorization headers to bypass network unauthorized errors. 

### 3. Parallel Python Infrastructure
- **`casper_deployer.py` & `casper_merkle_builder.py`**: Interacts with the `casper-client` CLI via Python subprocesses. 
- *Zero-Disruption Design*: Designed to run perfectly parallel to our existing LitVM and Mantle infrastructure without disrupting ongoing operations.

---

## 📦 Usage

### Prerequisites
- [cargo-odra](https://github.com/odradev/cargo-odra)
- Python 3.11+
- `casper-client` CLI

### Build the WASM Contract
```bash
cargo odra build -b casper
```
*The compiled binaries will be output to `/wasm`.*

### Run Local Tests
```bash
cargo odra test
```

### Deployment via Proxy
First, start the proxy to authenticate your node connection:
```bash
python casper_proxy.py
```
Then execute the deployment pipeline:
```bash
python casper_deployer.py
```

---

## 🔒 Security
- **PEM Vaulting**: Deployment relies on local `.pem` key generation, which is strictly `.gitignore`'d and securely mounted.
- **Stateless Proxy**: The RPC proxy never stores private keys in memory—it merely injects CDP auth headers for transport.

---

## 📝 License

Licensed under the **[Business Source License 1.1 (BUSL-1.1)](LICENSE)** by **The Undesirables LLC**.  
Free for personal, educational, and agentic integrations. Commercial operation of competing on-chain price oracle services requires a commercial license.
