import os
import sys
import json
import sqlite3
import subprocess
from datetime import datetime, timezone
from web3 import Web3
from eth_abi import encode as abi_encode

DB_PATH = os.path.expanduser("~/.cache/market_memory.sqlite")
NODE_RPC = "http://127.0.0.1:7777"
CHAIN_NAME = "casper-test"

def keccak256(data: bytes) -> bytes:
    return Web3.keccak(data)

def compute_leaf(product_id: int, category_id: int, name: str, market_price: int, low_price: int) -> bytes:
    inner = abi_encode(["uint256", "uint16", "string", "uint256", "uint256"],
                       [product_id, category_id, name, market_price, low_price])
    return keccak256(keccak256(inner))

def build_merkle_tree(leaves: list[bytes]) -> tuple[bytes, list[list[bytes]]]:
    padded = list(leaves)
    while len(padded) & (len(padded) - 1): padded.append(b"\x00" * 32)
    if len(padded) == 1: padded.append(b"\x00" * 32)
    tree = [padded]
    current = padded
    while len(current) > 1:
        next_level = []
        for i in range(0, len(current), 2):
            left = current[i]
            right = current[i + 1] if i + 1 < len(current) else b"\x00" * 32
            pair = left + right if left < right else right + left
            next_level.append(keccak256(pair))
        tree.append(next_level)
        current = next_level
    return current[0], tree

def load_products(db_path: str):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    latest_date = cursor.execute("SELECT MAX(date) FROM price_history").fetchone()[0]
    rows = cursor.execute("""
        SELECT p.product_id, c.category_id, c.name, CAST(p.market_price * 100 AS INTEGER), CAST(p.low_price * 100 AS INTEGER)
        FROM price_history p JOIN cards c ON p.product_id = c.product_id
        WHERE p.date = ? AND p.market_price > 0 ORDER BY p.product_id ASC
    """, (latest_date,)).fetchall()
    conn.close()
    return rows, latest_date

def push_to_casper(root: bytes, contract_hash: str, key_path: str):
    print("Pushing root to Casper Testnet via CLI...")
    root_hex = root.hex()
    cmd = [
        "/Users/davidluna/.cargo/bin/casper-client", "put-deploy",
        "--node-address", NODE_RPC,
        "--chain-name", CHAIN_NAME,
        "--secret-key", key_path,
        "--payment-amount", "1000000000",  # 1 CSPR gas
        "--session-hash", contract_hash,
        "--session-entry-point", "update_root",
        "--session-arg", f"new_root:byte_array='{root_hex}'"
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Root successfully sent to Casper!")
        print(result.stdout)
    else:
        print("❌ Failed to push root!")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", required=True, help="Path to secret_key.pem")
    parser.add_argument("--contract", required=True, help="Contract hash string (e.g. hash-...)")
    args = parser.parse_args()
    
    print("Building Merkle tree from SQLite...")
    products, date = load_products(DB_PATH)
    leaves = [compute_leaf(*p) for p in products]
    root, _ = build_merkle_tree(leaves)
    print(f"Merkle Root: 0x{root.hex()}")
    
    push_to_casper(root, args.contract, args.key)
