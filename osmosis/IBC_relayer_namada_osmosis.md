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
