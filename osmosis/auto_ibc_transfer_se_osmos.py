#!/usr/bin/expect -f

# Use the system crontab to call this Python script, which automatically triggers the Namada IBC transfer command to send 1 naan from Namada testnet to the Osmosis testnet, thereby testing the availability of the IBC Relayer.
# How to set up crontab to launch this script. There is an example.
# execute command: crontab -e
# Add a line at the end of the file which indicates to execute every 10 minutes between 3 AM and 4 AM UTC, for a total of 6 times.
# */6 3 * * * /usr/bin/unbuffer /home/user/auto_ibc_transfer_se_osmos.py


# Set up environment variables for Namada
# Your Namada sender wallet password
set password "PASSWORD"
# Namada SE BASE_DIR
set base_dir "$env(HOME)/.local/share/namada"
# Namada Sender wallet address 
set source_addr "Your_Namada_sender_address"
# Osmosis Receiver wallet address 
set receiver_addr "Your_Osmos_receiver_address"
# IBC Relayer Channel on Namada side
set channel "Channel_ID"
# Namada RPC node
set rpc_node "http://IP:PORT"
# Namada sender public key
set wallet_pk
# The minimum balance required to be maintained in a Namada sender wallet
set threshold 0

# Check current balance of Namada sender
spawn namadac balance --owner $source_addr --node $rpc_node
expect -re {naan: (\d+)}
set number $expect_out(1,string)

# Ensure that the naan in the sender wallet is greater than 0
if {$number > $threshold} {
    puts "The amount of naan is: $number"
    puts "IBC transfer 1 naan from $source_addr to $receiver_addr"
    spawn namadac --base-dir $base_dir ibc-transfer --amount 1 --source $source_addr --receiver $receiver_addr --token naan --channel-id $channel --node $rpc_node --memo $wallet_pk
    expect "Enter decryption password:"
    send "$password\r"
    interact
} else {
    puts "The amount of naan is not greater than $threshold, please fund more faucets."
}
