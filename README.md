<div align="center">

<img src="https://raw.githubusercontent.com/sailorpepe/undesirables-x402-server/main/assets/banner.png" alt="TCG Oracle Banner" width="100%" />

# ⛓️ Casper TCG Oracle (Merkle Price Oracle)

**Agentic Buildathon Phase 1 & 2 • Odra WASM Smart Contracts • Python Deployment Proxy**

![Rust](https://img.shields.io/badge/Rust-000000?style=flat-square&logo=rust&logoColor=white)
![Casper Network](https://img.shields.io/badge/Chain-Casper_Testnet-FF0000?style=flat-square&logo=casper&logoColor=white)
![Odra](https://img.shields.io/badge/Framework-Odra-blue?style=flat-square)
![License: BSL-1.1](https://img.shields.io/badge/License-BSL_1.1-red?style=flat-square)

[Contract Explorer (Testnet)](https://testnet.cspr.live/contract/0235f90c8dac5ecb30011672fc60ce1e98d51c5adfb5c019f44622bfb344bd77) · [x402 Server Integration](https://github.com/sailorpepe/undesirables-x402-server)

</div>

---

## ⚡ Overview

This repository houses the **Merkle Price Oracle** for the **Casper Testnet**, built as part of the Agentic Buildathon. It provides trustless, on-chain verification for over 276,000 Trading Card Game (TCG) products and connects directly to the [LitVM x402 Server ecosystem](https://github.com/sailorpepe/undesirables-x402-server).

By committing the Merkle root of our price database to Casper daily, any agent can independently verify a card's price on-chain without trusting our off-chain API. Prices come from our **conformal-calibrated risk oracle** — regime-aware split-conformal price bands with honest Value-at-Risk by default; Monte Carlo (Merton jump-diffusion) is available opt-in via `model=`.

---

## 🏗️ Architecture

### 1. Smart Contract (Rust / Odra)
- **`src/merkle_oracle.rs`**: Core price verification logic. Takes a Merkle root and allows verification of TCG price proofs directly on the Casper network.
- **The Database Contract**: We upload the compressed Merkle Root of our entire **276,000+ product database** to the [Merkle Price Oracle Contract (Testnet)](https://testnet.cspr.live/contract/0235f90c8dac5ecb30011672fc60ce1e98d51c5adfb5c019f44622bfb344bd77) daily. This trustless design allows any agent to independently verify a card's price on-chain without trusting our off-chain API.
- **WASM Build**: Compiled down to a secure `MerklePriceOracle.wasm` binary using `cargo odra build`.

### 2. Secure Deployment Proxy
- **`casper_proxy.py`**: A custom HTTP middleware proxy that safely routes local JSON-RPC requests to `node.testnet.cspr.cloud/rpc`, seamlessly injecting CSPR API authorization headers to bypass network unauthorized errors. 

### 3. Parallel Python Infrastructure
- **`casper_deployer.py` & `casper_merkle_builder.py`**: Interacts with the `casper-client` CLI via Python subprocesses. 
- *Zero-Disruption Design*: Designed to run perfectly parallel to our existing LitVM and Mantle infrastructure without disrupting ongoing operations.

### 4. x402 Server API Endpoints
The backend [x402 Server](https://github.com/sailorpepe/undesirables-x402-server) exposes a Casper-anchored price endpoint behind the standard x402 payment gate:
- **`GET /api/v1/casper/price`**: An agent requests a specific card's price and receives price data **anchored to the on-chain Casper Merkle root** — independently verifiable against the contract ([`0235f90c…`](https://testnet.cspr.live/contract/0235f90c8dac5ecb30011672fc60ce1e98d51c5adfb5c019f44622bfb344bd77)) without trusting our API. Access is gated by the oracle's standard **x402 HTTP 402 challenge (USDC on Base)**. *The Casper contribution is the on-chain price Merkle root, not a CSPR-native payment leg — the 402 gate is live and demoable; native-CSPR settlement is not implemented.*
- Automatically handles wallet signature authentication for the Casper Network via the local `.pem` vault.

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
