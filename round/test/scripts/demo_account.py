# demo_account.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import round.test.scripts.helpers as helpers

import yaml
import os.path

import round

import time


def current_milli_time():
    return int(round(time.time()))


wallet_file = helpers.wallet_file()
if os.path.isfile(wallet_file):
    with open(wallet_file, u'r') as file:
        data = yaml.load(file)
    address = data[u'node'][u'address']
    message = u'''
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

record = {}

client = round.client(helpers.round_url())
users = client.users

email = u'matthew-{0}@gem.co'.format(current_milli_time())
password = u'horriblepassword'

user = users.create(email=email, password=password)
record[u'user'] = dict(email=email, password=password)

application = user.applications.create(
    name=u'bitcoins_r_us',
    callback_url=u'https://someapp.com/callback')

record[u'api_token'] = application.api_token
record[u'application'] = dict(url=application.url)

client.context.set_application(url=application.url, token=application.api_token)



passphrase = u"wrong pony generator brad"
record[u'passphrase'] = passphrase

backup_seed, wallet = application.wallets.create(
    passphrase=passphrase, name=u'my favorite')

record[u'wallet'] = {u'url': wallet.url}

account = wallet.accounts.create(name=u'office supplies')
record[u'account'] = {u'url': account.url}

address = account.addresses.create()
record[u'node'] = {u'path': address.path, u'address': address.string}

print "List addresses for the account"
for address in account.addresses:
    print repr(address)

# save YAML record to file.

with open(helpers.wallet_file(), u'w') as file:
    yaml.safe_dump(record, file)

message = u'''
    Fund this address from a testnet faucet, so that you can make payments or transfers:
    {0}

    Suggested faucet:  http://faucet.xeno-genesis.com
    Once the transaction is confirmed (with 6 blocks) run demo_payment.rb

    You can check the state of transactions for the address at:
    http://tbtc.blockr.io/address/info/{0}
    '''.format(address.string)

print message
