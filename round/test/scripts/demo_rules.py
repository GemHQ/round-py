
import os.path
import yaml

import round.test.scripts.helpers as helpers

import round


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

user = data[u'user']
api_token = data[u'api_token']
passphrase = data[u'passphrase']
app_url = data[u'application'][u'url']
wallet_url = data[u'wallet'][u'url']

client = round.authenticate(url=helpers.round_url(), developer=user)
client.context.authorize(u'Gem-Application', url=app_url, token=api_token)

application = client.application
wallet = client.wallet(wallet_url)
account = wallet.accounts['office supplies']

try:
    whitelist = application.rules['gem:whitelist']
except KeyError:
    whitelist = application.rules.add('gem:whitelist')


address_payee = dict(
        type='address',
        value='mp1vqX3gEH9dTXvFL7d36FtBCQQWSGusnG',
        memo='testnet faucet return'
        )

wallet_payee = dict(
        type='wallet',
        value=wallet,
        )

whitelist = whitelist.set(
        {'faucet': address_payee}
        )

result = whitelist.delete()



