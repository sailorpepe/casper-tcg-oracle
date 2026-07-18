# Testing Playbook — Casper TCG Oracle

Step-by-step instructions to independently verify this submission. No account,
wallet, or payment is required for Steps 1–5.

## What this MVP does (the claim you are verifying)

Every hour we build a Merkle tree over ~284,000 trading-card price rows and commit
the **root** to an Odra/Rust smart contract on **Casper Testnet**. Because the root
is on-chain *before* anyone queries it, any agent can verify that a card's price is
the one we committed — without trusting our off-chain API. Casper's role is the
**trust anchor** (the on-chain root); price *access* is gated by our x402 API.

Canonical references:
- **Contract:** `0235f90c8dac5ecb30011672fc60ce1e98d51c5adfb5c019f44622bfb344bd77`
- **Explorer:** https://testnet.cspr.live/contract/0235f90c8dac5ecb30011672fc60ce1e98d51c5adfb5c019f44622bfb344bd77
- **Source:** https://github.com/sailorpepe/casper-tcg-oracle

---

## Step 1 — Verify the deployed contract on-chain (no tools)

Open the explorer link above. Confirm:
- The contract exists on **casper-test** and is owned by our deployer account.
- It exposes a named key / entry points consistent with the source
  (`init`, `update_root`, `get_root` in `src/merkle_oracle.rs`).

## Step 2 — Verify a sample deploy transaction

Deploy hash (initial contract install, 2026-06-10):
```
f881a05f49ddbc0bfd108ab95c1540af6e2fb9d8843c74de48b084188dfa7de0
```
View: https://testnet.cspr.live/deploy/f881a05f49ddbc0bfd108ab95c1540af6e2fb9d8843c74de48b084188dfa7de0
Confirm status **Success** on chain `casper-test`.

## Step 3 — Inspect the current Merkle root

A recent hourly root-commit deploy (2026-07-18):
```
07db0bd24c4c28d731ab7555ceb8d1046f5a3cae6e36c39abdb2182c735641b2
```
The on-chain `merkle_root` value it wrote:
```
0xab759847e136ed63c8cee15ab2f00d57e15ca60edff7f347440757c768b2ba0e
```
Confirm the deploy executed **Success**. To read the committed root straight
from the deploy itself (the contract stores state in Odra's internal
dictionary, so a plain named-key query won't find it — the session args are
the honest, judge-friendly source):
```bash
casper-client get-deploy --node-address <RPC> <deploy_hash> \
  | python3 -c "import json,sys; \
    args=json.load(sys.stdin)['result']['deploy']['session']['StoredContractByHash']['args']; \
    print([v.get('parsed') for n,v in args if n=='new_root'][0])"
```
(The root changes hourly as prices update — this is the point: fresh, timestamped,
on-chain. To verify independently, rebuild the tree from the public dataset with
`casper_merkle_builder.py` and compare roots.)

## Step 4 — Build & test the contract locally

```bash
git clone https://github.com/sailorpepe/casper-tcg-oracle.git
cd casper-tcg-oracle

# Toolchain is pinned in ./rust-toolchain (nightly-2026-01-01)
cargo test --lib          # runs the contract unit tests on the Odra mock backend
cargo odra build -b casper # compiles MerklePriceOracle.wasm (requires cargo-odra)
```
Expected: unit tests pass (`test_initialization`, `test_update_root`); the WASM
binary is produced in `wasm/`. CI runs the same `cargo test --lib` on every push.

## Step 5 — Observe the x402 payment gate (live)

An unpaid request returns an **HTTP 402** challenge with machine-readable payment
instructions (this is the standard x402 rail, **USDC on Base** — the same rail as
the rest of the oracle):
```bash
curl -si "https://oracle.the-undesirables.com/api/v1/casper/price?query=charizard" | head -n 20
```
Expected: `HTTP/2 402` plus a JSON body describing the required payment and the
Casper contract the price is anchored to.

## Step 6 — (Optional) Recompute a leaf to verify the trust model

The leaf format the builder uses (`casper_merkle_builder.py`) is deterministic and
third-party-recomputable:
```
leaf = keccak256( keccak256( abi_encode(
          uint256 product_id, uint16 category_id, string name,
          uint256 market_price_cents, uint256 low_price_cents ) ) )
```
Pairs are hashed sorted (`min||max`), and the level is zero-padded to a power of two.
Recomputing a card's leaf and its path should reproduce the on-chain root from
Step 3 — meaning the price you were served is provably the committed one.

---

## Honest scope (what this is and isn't)

- **Is:** a live Odra/Rust contract on Casper Testnet holding an hourly, verifiable
  Merkle root over a real 284K-row TCG price database; reproducible build + tests;
  a live x402-gated read endpoint.
- **Isn't:** a native-CSPR payment leg. Payment settlement runs on the existing
  x402 USDC-on-Base rail; Casper's contribution here is the **on-chain price
  anchor**, not a CSPR micropayment flow. We'd rather state that plainly than
  overclaim.
