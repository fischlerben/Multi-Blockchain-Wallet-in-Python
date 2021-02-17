import subprocess
import json
from constants import *

import os
from web3 import Web3
from web3.middleware import geth_poa_middleware

from eth_account import Account
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

load_dotenv()

w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:8545'))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

mnemonic = os.getenv('mnemonic', 'eager exercise miss ivory brief despair ranch brief common glide all manual')

# This function will call the ./derive script
def derive_wallets():

    command = f'./derive -g --mnemonic="{mnemonic}" --coin="{coin}" --numderive="{numderive}" --cols=address,index,path,address,privkey,pubkey,pubkeyhash,xprv,xpub --format=json'

    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()

    keys = json.loads(output)
    return (keys)

coins = {
    "btc-test" : derive_wallets(mnemonic, BTCTEST, 3),
    "eth": derive_wallets(mnemonic, ETH, 3)
    }

# This function converts privkey string to an account object that bit or web3.py can use to make transactions:
def priv_key_to_account(coin, priv_key):

    if(coin == 'eth'):
        return Account.privateKeyToAccount(priv_key)
    elif(coin == 'btc-test'):
        return PrivateKeyTestnet(priv_key)


# This function creates raw, unsigned transaction:
def create_tx(coin, account, to, amount):

    if(coin == 'eth'):
        gas_estimate = w3.eth.estimateGas(
            {'from': account.address, 'to': to, 'value': amount}
        )
        return {
            'from': account.address,
            'to': to,
            'value': amount,
            'gasPrice': w3.eth.gasPrice,
            'gas': gas_estimate,
            'nonce': w3.eth.getTransactionCount(account.address)
        }
    elif(coin == 'btc-test'):
        return PrivateKeyTestnet.prepare_transaction(account.address, [(to, amount, BTC)])

# This function signs transaction and sends to network:
def send_tx(coin, account, to, amount):
    raw_tx = create_tx(coin, account, to, amount)
    signed = account.sign_transaction(raw_tx)
    if(coin == 'eth'):
        return w3.eth.sendRawTransaction(signed.rawTransaction)
    elif(coin == 'btc-test'):
        return NetworkAPI.broadcast_tx_testnet(signed)

# To send ETH transaction:
eth_sender_account = priv_key_to_account(ETH,coins["eth"][0]['privkey'])
eth_recipient_address = coins["eth"][1]["address"]

send_tx(ETH, eth_sender_account, eth_recipient_address, 2)

# To send Bitcoin Testnet transaction:
btctest_sender_account = priv_key_to_account(BTCTEST,coins["btc-test"][0]['privkey'])
btctest_recipient_address = coins["btc-test"][1]["address"]

send_tx(BTCTEST, btctest_sender_account, btctest_recipient_address, .0001)
