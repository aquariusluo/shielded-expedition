# Operate a shielded expedition-compatible Osmosis testnet relayer

## Deploy a full node for Osmosis testnet which chain-id is `osmo-test-5`

## Deploy Hermes
- Build hermes via source code
```
export TAG="v1.7.4-namada-beta7"
cd $HOME && git clone https://github.com/heliaxdev/hermes.git && cd hermes && git checkout $TAG
cargo build --release --bin hermes
sudo cp target/release/hermes /usr/local/bin/
hermes --version
```
