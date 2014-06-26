# demo_payment.py
#
# Copyright 2014 BitVault.


import os.path
import yaml

import bitvault.test.scripts.helpers as helpers

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

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

# OR
#client = bitvault.authenticate(user={'email': email, 'password': password})


# These methods don't exist in the Ruby client yet.
wallet = client.wallet(wallet_url)
account = wallet.accounts.find('office supplies')


exit()

faucet_address = u'mx3Az5tkWhEQHsihFr3Nmj6mRHLeqtqfNK'

primary_seed = PassphraseBox.decrypt(passphrase, wallet.primary_private_seed)

# FIXME: imitate the Ruby client's account.pay method
# https://github.com/BitVault/bitvault-rb/blob/new-interface/test/scripts/client_usage_improved.rb#L90

payment = account.pay([
        { 'address': faucet_address, 'amount': 6000000 }
    ])


#transaction = Transaction.from_data(unsigned_payment)
#change_output = transaction.outputs[-1]

#multi_wallet.is_valid_output(change_output)

#signatures = multi_wallet.signatures(transaction)

