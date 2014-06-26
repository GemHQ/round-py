# demo_payment.py
#
# Copyright 2014 BitVault.


import os.path
import yaml

import bitvault.test.scripts.helpers as helpers

from coinop.crypto.passphrasebox import PassphraseBox

import bitvault


wallet_file = helpers.wallet_file()

if not os.path.isfile(wallet_file):
    message = u'''
    This script requires output from demo_account.rb, which will be
    found in {0}.
    Run demo_account.rb first, then fund the address provided using
    a testnet faucet.  Once the transaction has 3 confirmations,
    you should be able to run this script.
    '''.format(wallet_file)
else:
    with open(wallet_file, u'r') as file:
        data = yaml.load(file)

api_token = data[u'api_token']
passphrase = data[u'passphrase']
app_url = data[u'application'][u'url']
wallet_url = data[u'wallet'][u'url']
account_url = data[u'account'][u'url']

client = bitvault.authenticate(application={'url': app_url, 'token': api_token})


wallet = client.wallet(wallet_url)
wallet.unlock(passphrase)
account = wallet.accounts.find('office supplies')

faucet_address = u'mx3Az5tkWhEQHsihFr3Nmj6mRHLeqtqfNK'


payment = account.pay([
        { 'address': faucet_address, 'amount': 6543000 }
    ])

print 'payment submitted', repr(payment.hash)



