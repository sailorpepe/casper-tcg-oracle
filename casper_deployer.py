import os
import sys
import subprocess

# Casper Testnet configuration
NODE_RPC = "http://127.0.0.1:7777"
CHAIN_NAME = "casper-test"

def deploy_contract(wasm_path: str, private_key_path: str):
    if not os.path.exists(wasm_path):
        print(f"ERROR: Wasm file not found at {wasm_path}")
        sys.exit(1)
        
    print(f"Deploying {wasm_path} using official Casper CLI...")
    cmd = [
        "/Users/davidluna/.cargo/bin/casper-client", "put-deploy",
        "--node-address", NODE_RPC,
        "--chain-name", CHAIN_NAME,
        "--secret-key", private_key_path,
        "--payment-amount", "100000000000",  # 100 CSPR gas
        "--session-path", wasm_path
    ]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Contract deployed successfully!")
        print(result.stdout)
        print("Wait ~30 seconds for the block to finalize.")
    else:
        print("❌ Deployment failed!")
        print(result.stderr)
        sys.exit(1)

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--wasm", default="wasm/MerklePriceOracle.wasm")
    parser.add_argument("--key", required=True, help="Path to secret_key.pem")
    args = parser.parse_args()
    deploy_contract(args.wasm, args.key)
