# Operate a shielded expedition-compatible Cosmos testnet relayer

# Install Cosmoshub testnet CLI
Cosmoshub testnet  
gaiad v14.1.0  
Chain ID: theta-testnet-001  

# Generate cosmos relayer and get faucet
```
gaiad keys add "relayer_cosmos"
- name: relayer_cosmos
  type: local
  address: cosmos1c0cq0ujddy0cq0vxuv42wylglvgp85y5gyucg7
  pubkey: '{"@type":"/cosmos.crypto.secp256k1.PubKey","key":"AlXGODCzh1JIOJDnFlvbmEEkzz7ZLHrAMSM52zSd2aHf"}'
  mnemonic: ""
**Important** write this mnemonic phrase in a safe place.
It is the only way to recover your account if you ever forget your password.

jeans equip blind shy noble umbrella sadness auction angle ride fly dirt enlist rural arctic snake cable elevator luxury differ pair churn delay only
```
```
gaiad query bank balances cosmos1c0cq0ujddy0cq0vxuv42wylglvgp85y5gyucg7 --chain-id theta-testnet-001 --node http://localhost:36657
balances:
- amount: "6000000"
  denom: uatom
pagination:
  next_key: null
  total: "0"

namadac balance --owner relayer_se --node http://94.130.90.47:26657
naan: 244.5
transfer/channel-259/uosmo: 1000000
transfer/channel-90/uosmo: 1000000
```

```
hermes --config $HERMES_CONFIG \
  create channel \
  --a-chain shielded-expedition.88f17d1d14 \
  --b-chain theta-testnet-001 \
  --a-port transfer \
  --b-port transfer \
  --new-client-connection --yes
SUCCESS Channel {
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
            "07-tendermint-1823",
        ),
        connection_id: ConnectionId(
            "connection-787",
        ),
        port_id: PortId(
            "transfer",
        ),
        channel_id: Some(
            ChannelId(
                "channel-519",
            ),
        ),
        version: None,
    },
    b_side: ChannelSide {
        chain: BaseChainHandle {
            chain_id: ChainId {
                id: "theta-testnet-001",
                version: 0,
            },
            runtime_sender: Sender { .. },
        },
        client_id: ClientId(
            "07-tendermint-3247",
        ),
        connection_id: ConnectionId(
            "connection-3411",
        ),
        port_id: PortId(
            "transfer",
        ),
        channel_id: Some(
            ChannelId(
                "channel-3913",
            ),
        ),
        version: None,
    },
    connection_delay: 0ns,
}
```
