# Multi-Blockchain Wallet in Python
This example takes you through the steps needed to create a "universal" wallet that supports many different cryptocurrencies.  This tool will allow you to manage billions of addresses across hundreds of different coins.  Specifically, an Ethereum and Bitcoin Testnet are generated in this example.

## Dependencies:
- PHP must be installed on your operating system (any version, 5 or 7). Don't worry, you will not need to know any PHP.
- You will need to clone the hd-wallet-derive tool.
- bit Python Bitcoin library.
- web3.py Python Ethereum library.

## Steps to Generate Multi-Blockchain Wallet in Python:

1. Create a project directory called wallet and cd into it.

2. Clone the hd-wallet-derive tool into this folder and install it using the instructions on its README.md.
![cloning_hd_derive](/Screenshots/cloning_hd_derive.png?raw=true)

3. Create a symlink called derive for the hd-wallet-derive/hd-wallet-derive.php script into the top level project directory like so: ln -s hd-wallet-derive/hd-wallet-derive.php derive
![creating_symlink_in_wallet_folder](/Screenshots/creating_symlink_in_wallet_folder.png?raw=true)

4. Test that you can run the ./derive script properly, use one of the examples on the repo's README.md
![test_script_from_repo](/Screenshots/test_script_from_repo.png?raw=true)

5. Create a file called wallet.py -- this will be your universal wallet script.  My final wallet.py file is located above in the "wallet" folder, but here is a snippet of the beginning of my wallet.py file:
![creating_wallet_file](/Screenshots/creating_wallet_file.png?raw=true)

6. Setup Constants:
![creating_constants_file](/Screenshots/creating_constants_file.png?raw=true)

At this point, I followed the rest of the instructions to flesh out my wallet.py file and include everything it needed, including the functions, the variables, etc.

### Send some transactions!

Now, you should be able to fund these wallets using testnet faucets. Open up a new terminal window inside of wallet, then run python. Within the Python shell, run from wallet import * -- you can now access the functions interactively.  You'll need to set the account with  priv_key_to_account and use send_tx to send transactions:

    btctest_sender_account = priv_key_to_account(BTCTEST,coins["btc-test"][0]['privkey'])
    btctest_recipient_address = coins["btc-test"][1]["address"]
    send_tx(BTCTEST, btctest_sender_account, btctest_recipient_address, .0001)

![wallet_code](/Screenshots/wallet_code.png?raw=true)

Per the instructions, I then funded a BTCTEST address using a testnet faucet (https://bitcoinfaucet.uo1.net/send.php), sent a transaction to another testnet address, and used a block explorer (https://tbtc.bitaps.com/)to watch this transaction:

![sending_btc](/Screenshots/sending_btc.png?raw=true)

![confirmed_send](/Screenshots/confirmed_send.png?raw=true)


### Local PoA Ethereum Transaction:

1. Add one of the ETH addresses to the pre-allocated accounts in your networkname.json (don't include 0x at beginning) - my new address that I added is highlighted:

![pre_funded](/Screenshots/pre_funded.png?raw=true)

2. Delete the geth folder in each node, then re-initialize using geth --datadir nodeX init networkname.json.  This will create a new chain, and will pre-fund the new account:

![new_fund](/Screenshots/new_fund.png?raw=true)

3. Add the following middleware to support the PoA algorithm:
from web3.middleware import geth_poa_middleware
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

Due to a bug in web3.py, you will need to send a transaction or two with MyCrypto first, since the
w3.eth.generateGasPrice() function does not work with an empty chain. You can use one of the ETH address privkey,
or one of the node keystore files.

4. Send a transaction from the pre-funded address within the wallet to another (I did mine within MyCrypto), then copy the txid into MyCrypto's TX Status, and screenshot the successful transaction:

    eth_sender_account = priv_key_to_account(ETH,coins["eth"][0]['privkey'])
    eth_recipient_address = coins["eth"][1]["address"]
    send_tx(ETH, eth_sender_account, eth_recipient_address, 2)

![hash](/Screenshots/hash.png?raw=true)

As you can see in the above, similar to the other assignment involving MyCrypto, I seem to be unable to get my transaction to move from "Pending" to "Complete."