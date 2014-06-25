# low_demo_account.py
#
# Copyright 2014 BitVault.


import bitvault.test.scripts.helpers as helpers

import yaml
import os.path

wallet_file = helpers.wallet_file()
if os.path.isfile(wallet_file):
    with open(wallet_file, u'r') as file:
        data = yaml.load(file)
    address = data['node']['address']
    message = '''
    Settings from a previous run of this script are in {0}.
    If you have not already funded that wallet, you can remove the file.
    Otherwise, fund this address:
    {1}
    then run demo_payment.rb
    You can check the state of transactions for the address at:
    http://tbtc.blockr.io/address/info/{1}
    '''.format(wallet_file, address)
    print message
    exit(0)



from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet


import time
current_milli_time = lambda: int(round(time.time()))

record = {}

bitvault = helpers.bitvault()
client = bitvault.spawn()
resources = client.resources
users = resources.users

email = 'matthew-{0}@bitvault.io'.format(current_milli_time())
content = {'email': email, 'password': 'horriblepassword'}
user = users.create(content)

client.context.set_basic(email, 'horriblepassword')

application = user.applications.create({'name': 'bitcoins_r_us'})

record['api_token'] = application.api_token

client.context.set_token(application.api_token)

application.wallets.list()

multi_wallet = MultiWallet.generate(["primary", "backup"])
primary_seed = multi_wallet.private_seed("primary")
primary_public_seed = multi_wallet.public_seed('primary')
backup_public_seed = multi_wallet.public_seed('backup')

passphrase = "wrong pony generator brad"
record['passphrase'] = passphrase

encrypted_seed = PassphraseBox.encrypt(passphrase, primary_seed)

content = {'name': 'my favorite', 'network': 'bitcoin_testnet',
        'backup_public_seed': backup_public_seed,
        'primary_public_seed': primary_public_seed,
        'primary_private_seed': encrypted_seed}

wallet = application.wallets.create(content)
record['wallet'] = {'url': wallet.url}

account = wallet.accounts.create({'name': 'office supplies'})
record['account'] = {'url': account.url}

address = account.addresses.create()
record['node'] = {'path': address.path, 'address': address.string}

# save YAML record to file.

with open(helpers.wallet_file(), u'w') as file:
    yaml.safe_dump(record, file)

message = '''
    Fund this address from a testnet faucet, so that you can make payments or transfers:
    {0}

    Suggested faucet:  http://faucet.xeno-genesis.com
    Once the transaction is confirmed (with 6 blocks) run demo_payment.rb

    You can check the state of transactions for the address at:
    http://tbtc.blockr.io/address/info/{0}
    '''.format(address.string)

print message
