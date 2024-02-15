# Operate a shielded expedition-compatible Osmosis testnet relayer

## Deploy a full node for Osmosis testnet which chain-id is `osmo-test-5`

## Setup enviroment variates
export CHAIN_ID_A="shielded-expedition.88f17d1d14"  
export CHAIN_ID_B="osmo-test-5"  
export BASE_DIR_A="$HOME/.local/share/namada"  
export BASE_DIR_B="$HOME/.osmosisd"  
export HERMES_DIR="$HOME/.hermes"  
export HERMES_CONFIG="$HERMES_DIR/config.toml"  

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

## Install Namada
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




