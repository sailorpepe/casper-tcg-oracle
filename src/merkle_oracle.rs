use odra::prelude::*;

#[odra::odra_error]
pub enum Error {
    NotOwner = 1,
}

#[odra::module]
pub struct MerklePriceOracle {
    owner: Var<Address>,
    merkle_root: Var<[u8; 32]>,
}

#[odra::module]
impl MerklePriceOracle {
    pub fn init(&mut self) {
        self.owner.set(self.env().caller());
        self.merkle_root.set([0u8; 32]);
    }

    pub fn update_root(&mut self, new_root: [u8; 32]) {
        if self.env().caller() != self.owner.get().unwrap() {
            self.env().revert(Error::NotOwner);
        }
        self.merkle_root.set(new_root);
    }

    pub fn get_root(&self) -> [u8; 32] {
        self.merkle_root.get_or_default()
    }
}

#[cfg(test)]
mod tests {
    use crate::merkle_oracle::{MerklePriceOracle, Error};
    use odra::host::{Deployer, NoArgs};

    #[test]
    fn test_initialization() {
        let env = odra_test::env();
        let contract = MerklePriceOracle::deploy(&env, NoArgs);
        assert_eq!(contract.get_root(), [0u8; 32]);
    }

    #[test]
    fn test_update_root() {
        let env = odra_test::env();
        let mut contract = MerklePriceOracle::deploy(&env, NoArgs);
        let new_root = [1u8; 32];
        contract.update_root(new_root);
        assert_eq!(contract.get_root(), new_root);
    }
}
