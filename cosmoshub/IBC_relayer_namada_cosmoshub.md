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
