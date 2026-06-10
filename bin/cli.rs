//! This example demonstrates how to use the `odra-cli` tool to deploy and interact with a smart contract.

use casper_tcg_oracle::merkle_oracle::MerklePriceOracle;
use odra::host::{HostEnv, NoArgs};
use odra_cli::{
    deploy::DeployScript,
    CommandArg, ContractProvider, DeployedContractsContainer, DeployerExt,
    OdraCli, 
};

/// Deploys the `MerklePriceOracle` and adds it to the container.
pub struct OracleDeployScript;

impl DeployScript for OracleDeployScript {
    fn deploy(
        &self,
        env: &HostEnv,
        container: &mut DeployedContractsContainer
    ) -> Result<(), odra_cli::deploy::Error> {
        let _oracle = MerklePriceOracle::load_or_deploy(
            &env,
            NoArgs,
            container,
            350_000_000_000 // Adjust gas limit as needed
        )?;

        Ok(())
    }
}

/// Main function to run the CLI tool.
pub fn main() {
    OdraCli::new()
        .about("CLI tool for casper_tcg_oracle smart contract")
        .deploy(OracleDeployScript)
        .contract::<MerklePriceOracle>()
        .build()
        .run();
}
