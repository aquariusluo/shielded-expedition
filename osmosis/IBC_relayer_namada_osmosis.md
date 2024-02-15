# Operate a shielded expedition-compatible Osmosis testnet relayer

## Deploy a full node for Osmosis testnet which chain-id is `osmo-test-5`
Refer to Osmosis guideline.  
https://github.com/osmosis-labs/testnets/tree/main/testnets/osmo-test-5

## Setup enviroment variates
export CHAIN_ID_A="shielded-expedition.88f17d1d14"  
export CHAIN_ID_B="osmo-test-5"  
export BASE_DIR_A="$HOME/.local/share/namada"  
export BASE_DIR_B="$HOME/.osmosisd"  
export WALLET_PATH_A="$BASE_DIR_A/$CHAIN_ID_A/wallet.toml"
export HERMES_DIR="$HOME/.hermes"  
export HERMES_CONFIG="$HERMES_DIR/config.toml"  
export RPC_SE="94.130.90.47:26657"  
export RPC_OSMO="http://127.0.0.1:26657"  

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
Namada v0.31.4   
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
namadac balance --owner relayer_se --node $RPC_SE
naan: 30

osmosisd query bank balances osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
balances:
- amount: "100000000"
  denom: uosmo
```
## Configure hermes
mkdir $HERMES_DIR && cd $HERMES_DIR
```
sudo tee $HERMES_CONFIG > /dev/null <<EOF
[global]
log_level = 'info'
 
[mode]

[mode.clients]
enabled = true
refresh = true
misbehaviour = true

[mode.connections]
enabled = false

[mode.channels]
enabled = false

[mode.packets]
enabled = true
clear_interval = 10
clear_on_start = false
tx_confirmation = true

[telemetry]
enabled = false
host = '127.0.0.1'
port = 3001

[[chains]]
id = 'shielded-expedition.88f17d1d14'  # set your chain ID
type = 'Namada'
rpc_addr = 'http://94.130.90.47:26657'  # set the IP and the port of the chain
grpc_addr = 'http://94.130.90.47:9090'  # not used for now
event_source = { mode = 'push', url = 'ws://94.130.90.47:26657/websocket', batch_delay = '500ms' } 
account_prefix = ''  # not used
key_name = 'relayer_se'  # The key is an account name you made
store_prefix = 'ibc'
gas_price = { price = 0.0001, denom = 'tnam1qxvg64psvhwumv3mwrrjfcz0h3t3274hwggyzcee' } 
rpc_timeout = '30s'

[[chains]]
id = 'osmo-test-5'
type = 'CosmosSdk'
rpc_addr = 'http://127.0.0.1:26657'  # set the IP and the port of the chain
grpc_addr = 'http://127.0.0.1:9090'
event_source = { mode = 'push', url = 'ws://127.0.0.1:26657/websocket', batch_delay = '500ms' } 
account_prefix = 'osmo'
key_name = 'relayer_osmo'
address_type = { derivation = 'cosmos' }
store_prefix = 'ibc'
default_gas = 400000
max_gas = 120000000
gas_price = { price = 0.0025, denom = 'uosmo' }
gas_multiplier = 1.1
max_msg_num = 30
max_tx_size = 1800000
clock_drift = '15s'
max_block_time = '30s'
trusting_period = '4days'
trust_threshold = { numerator = '1', denominator = '3' }
rpc_timeout = '30s'
EOF
```
## Add the relayer keys to Hermes
echo "sadness gallery audit junk key hurt rifle vivid aisle nation fruit brain until track gasp mention before sting collect patch math resemble man limit" > ./mnemonic  
hermes --config $HERMES_CONFIG keys add --chain $CHAIN_ID_A --key-file $WALLET_PATH_A --overwrite  
hermes --config $HERMES_CONFIG keys add --chain $CHAIN_ID_B --mnemonic-file ./mnemonic --overwrite  

## Create IBC channel
```
hermes --config $HERMES_CONFIG \
  create channel \
  --a-chain $CHAIN_ID_A \
  --b-chain $CHAIN_ID_B \
  --a-port transfer \
  --b-port transfer \
  --new-client-connection --yes
```

<details>
    <summary> SUCCESS Channel </summary>
  
```
 {
    ordering: Unordered,
    a_side: ChannelSide {
        chain: BaseChainHandle {
            chain_id: ChainId {
                id: "shielded-expedition.88f17d1d14",
                version: 0,
            },
            runtime_sender: Sender { .. },
        },
        client_id: ClientId(
            "07-tendermint-354",
        ),
        connection_id: ConnectionId(
            "connection-149",
        ),
        port_id: PortId(
            "transfer",
        ),
        channel_id: Some(
            ChannelId(
                "channel-90",
            ),
        ),
        version: None,
    },
    b_side: ChannelSide {
        chain: BaseChainHandle {
            chain_id: ChainId {
                id: "osmo-test-5",
                version: 5,
            },
            runtime_sender: Sender { .. },
        },
        client_id: ClientId(
            "07-tendermint-2018",
        ),
        connection_id: ConnectionId(
            "connection-1959",
        ),
        port_id: PortId(
            "transfer",
        ),
        channel_id: Some(
            ChannelId(
                "channel-5600",
            ),
        ),
        version: None,
    },
    connection_delay: 0ns,
}

```
</details>

id: "shielded-expedition.88f17d1d14", channel_id: "channel-90"  
id: "osmo-test-5", channel_id: "channel-5600"  
export CHANNEL_ID_A="channel-90"  
export CHANNEL_ID_B="channel-5600"  

## IBC-tranfer 
Check balance before transfer
```
osmosisd query bank balances osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
balances:
- amount: "99989620"
  denom: uosmo

namadac balance --owner relayer_se --node $RPC_SE
naan: 12
```

Send naan from Namada to Osmosis
```
namadac --base-dir ${BASE_DIR_A} \
    ibc-transfer \
    --amount 1 \
    --source relayer_se \
    --receiver osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033 \
    --token naan \
    --channel-id ${CHANNEL_ID_A} \
    --node ${RPC_SE}

Wrapper transaction hash: 51151FA398F02EF7AB99B603895B1357C225785A7CA343817E7D5B76E90C346D
Inner transaction hash: F4A52E6382234111D0E712A66ACE758B842DB94A35CFE272A770E5D279080182
Wrapper transaction accepted at height 22673. Used 24 gas.
Waiting for inner transaction result...
Transaction was successfully applied at height 22674. Used 6193 gas.
```
Check balance after transfer, Succeed to receive "1" token by Osmosis wallet.
```
osmosisd query bank balances osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
balances:
- amount: "1"
  denom: ibc/05D9D8E7078C5573DD0E05F43F88CE0E01D532C3106D7E3D3FFB115AF6950548
- amount: "99989620"
  denom: uosmo

namadac balance --owner relayer_se --node $RPC_SE
naan: 8.5
```

Send uosmo from Osmosis to Namada
```
osmosisd tx ibc-transfer transfer \
  transfer \
  ${CHANNEL_ID_B} \
  tnam1qq7nfjqrsg8x9vssf87wamav883dw6eargagd763 \
  1000000uosmo \
  --from relayer_osmo \
  --gas auto \
  --gas-prices 0.025uosmo \
  --gas-adjustment 1.1 \
  --node ${RPC_OSMO} \
  --home ${BASE_DIR_B} \
  --chain-id osmo-test-5 \
  --yes
Enter keyring passphrase (attempt 1/3):
gas estimate: 120214
code: 0
codespace: ""
data: ""
events: []
gas_used: "0"
gas_wanted: "0"
height: "0"
info: ""
logs: []
raw_log: '[]'
timestamp: ""
tx: null
txhash: 3349121EEFA0A583468E113271E19119DC9F2EDF370B31053A705107CA6D5432
```
Check balance after transfer
```
namadac balance --owner relayer_se --node $RPC_SE
naan: 8.5
transfer/channel-90/uosmo: 1000000

osmosisd query bank balances osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
balances:
- amount: "1"
  denom: ibc/05D9D8E7078C5573DD0E05F43F88CE0E01D532C3106D7E3D3FFB115AF6950548
- amount: "98986614"
  denom: uosmo
```
Send naan from Namada to Osmosis with memo
```
namadac --base-dir ${BASE_DIR_A} \
    ibc-transfer \
    --amount 1 \
    --source relayer_se \
    --receiver osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033 \
    --token naan \
    --channel-id ${CHANNEL_ID_A} \
    --node ${RPC_SE} \
    --memo tpknam1qqjgef9zsd0gsyqn3af9nrgxyhapef3cjn5cyxpjcjgtq60de6502p8rf8h
Enter your decryption password: 
Transaction added to mempool.
Wrapper transaction hash: 65FD483C04CE457E7A615836B39726D653F916EEA76D00D6578E4CA45714574A
Inner transaction hash: 28C8F2A7D190FF7F912222E988DD2C6C020AFEC64656317A4417CD7FCD36944E
Wrapper transaction accepted at height 22807. Used 26 gas.
Waiting for inner transaction result...
Transaction was successfully applied at height 22808. Used 6193 gas.

osmosisd query bank balances osmo1z6m8ndunsc6kxyyjh0y2yr48s9lufv9caqe033
balances:
- amount: "2"
  denom: ibc/05D9D8E7078C5573DD0E05F43F88CE0E01D532C3106D7E3D3FFB115AF6950548
- amount: "98986614"
  denom: uosmo
```
