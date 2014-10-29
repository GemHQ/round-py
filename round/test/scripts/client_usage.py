# -*- coding: utf-8 -*-
# client_usage.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import time

import round


current_milli_time = lambda: int(round(time.time()))
email = '{0}@gem.co'.format(current_milli_time())
password = u'incredibly_secure'


## API discovery
#
# The BitVault server provides a JSON description of its API that allows
# the client to generate all necessary resource classes at runtime.

client = round.client(u'https://api-develop.gem.co')


## User management
#
# The create action returns a Developer Resource which has:
#
# * action methods (get, update, reset)
# * attributes (email, first_name, etc.)
# * associated resources (applications)

client.developers.create(email=email, password=password)

# Get an authenticated client representing the new developer
client = round.authed_client(email=email, password=password)
developer = client.developer


## Application management

## Fetch applications
#
# If the applications collection is not populated, it will be fetched from the
# server. The cached version will be used if it is already loaded. A refresh can
# be triggered by passing it as an option to the action.

developer.applications
developer.applications.refresh()


## Create an application.
#
# The optional callback_url attribute specifies a URL where Gem
# can POST event information such as confirmed transactions.

app = developer.applications.create(
    name=u'bitcoin_app',
    callback_url=u'https://someapp.com/callback')


## Users
#
# Users are associated with the Application that creates them, as well as any
# others they authorize.

user = app.users.create(
    email=u'someuser-{}@email.com'.format(current_milli_time()),
    first_name=u'someuser',
    last_name=u'jones')

## Wallets
#
#
wallet = user.wallets.create(passphrase=u'very insecure', name=u'my funds')


# An users' wallet collection is enumerable

 for wallet in app.wallets.values():
     print(wallet)


# And acts as a hash with names as keys

wallet = app.wallets[u'my funds']

## Accounts
#
# Wallets can have multiple accounts, each represented by a path in the
# MultiWallet's deterministic trees.

account = wallet.accounts.create(name=u'office supplies')


## Payments
#
# Sending payments

# Creating addresses for receiving payments
# This is a BIP 16 "Pay to Script Hash" address, where the script in question
# is a BIP 11 "multisig".

payment_address = account.addresses.create

# TODO: Additional method "prepare" to obtain unsigned transaction for inspection
payment = account.pay(payees=({u'address': payment_address, u'amount': 20000},))

## Transfers

account_1 = wallet.accounts[u'rubber bands']
account_2 = wallet.accounts.create(name=u'travel expenses')

wallet.transfer(amount=10000, source=account_1, destination=account_2)
