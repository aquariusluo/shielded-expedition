# Operate a shielded expedition-compatible Osmosis testnet relayer

## Deploy a full node for Osmosis testnet which chain-id is `osmo-test-5`

## Setup enviroment variates
export CHAIN_ID_A="shielded-expedition.88f17d1d14"  
export CHAIN_ID_B="osmo-test-5"  
export BASE_DIR_A="$HOME/.local/share/namada"  
export BASE_DIR_B="$HOME/.osmosisd"  
export HERMES_DIR="$HOME/.hermes"  
export HERMES_CONFIG="$HERMES_DIR/config.toml"  
export RPC_SE="94.130.90.47:26657"  
export RPC_OSMO="127.0.0.1:26657"

## Install Hermes
- Build hermes via source code
```
export TAG="v1.7.4-namada-beta7"
cd $HOME && git clone https://github.com/heliaxdev/hermes.git && cd hermes && git checkout $TAG
cargo build --release --bin hermes
sudo cp target/release/hermes /usr/local/bin/
hermes --version
```
- Create hermes service
```
sudo tee /usr/lib/systemd/user/hermesd.service > /dev/null <<EOF
[Unit]
Description=Hermes Daemon Service
After=network.target
StartLimitIntervalSec=60
StartLimitBurst=3

[Service]
Type=simple
Restart=always
RestartSec=30
ExecStart=/usr/local/bin/hermes --config $HOME/.hermes/config.toml start 

[Install]
WantedBy=default.target
EOF
```
sudo chmod 755 /usr/lib/systemd/user/hermesd.service  
systemctl --user daemon-reload  
systemctl --user enable hermesd  

## Install Namada CLI
```bash
cd $HOME && wget https://github.com/anoma/namada/releases/download/v0.31.4/namada-v0.31.4-Linux-x86_64.tar.gz  
tar -zxvf namada-v0.31.4-Linux-x86_64.tar.gz && cd ./namada-v0.31.4-Linux-x86_64  
sudo cp namada /usr/local/bin && sudo cp namadac /usr/local/bin && sudo cp namadaw /usr/local/bin && sudo cp namada /usr/local/bin  
cd $HOME && namada --version  
 -> Namada v0.31.4   
```
Join shielded expedition network  
```
cd $HOME && namada client utils join-network --chain-id $CHAIN_ID_A --dont-prefetch-wasm
```

## Create relayer accounts for Namada and Osmosis
Create relayer account for Namada SE
```
namadaw gen --alias relayer_se
Enter your encryption password: 
Enter same passphrase again: 
Using HD derivation path m/44'/877'/0'/0'/0'
Safely store your 24 words mnemonic.
country return ketchup used few mimic announce school share feature cluster sort night gate ghost decorate pull ankle empty pulse planet fan better shrimp
Successfully added a key and an address with alias: "relayer_se"

namadaw find --alias relayer_se
Found transparent keys:
  Alias "relayer_se" (encrypted):
    Public key hash: 3D34C803820E62B21049FCEEEFAC39E2D76B3D1A
    Public key: tpknam1qpscda50x8k3z6suzmhma834pkgw5dzdfh0vwqnzes8mawhdywtgwekeyrp
Found transparent address:
  "relayer_se": Implicit: tnam1qq7nfjqrsg8x9vssf87wamav883dw6eargagd763
```

Create relayer account for Osmosis
```
osmosisd keys add relayer_osmo
- address: osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
  name: relayer_osmo
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"A7qWbzb4VOei3kGtqPWHb3iD37z2pJlqs9+Sl+BgiGSV"}'
  type: local
**Important** write this mnemonic phrase in a safe place.
It is the only way to recover your account if you ever forget your password.
sadness gallery audit junk key hurt rifle vivid aisle nation fruit brain until track gasp mention before sting collect patch math resemble man limit
```

Faucet to relayer accounts and check balance
```

```

