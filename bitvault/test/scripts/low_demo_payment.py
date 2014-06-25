import os.path
import yaml

import bitvault.test.scripts.helpers as helpers

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet


wallet_file = helpers.wallet_file()

if not os.path.isfile(wallet_file):
    message = '''
    This script requires output from demo_account.rb, which will be
    found in {0}.
    Run demo_account.rb first, then fund the address provided using
    a testnet faucet.  Once the transaction has 3 confirmations,
    you should be able to run this script.
    '''.format(wallet_file)
else:
    with open(wallet_file, u'r') as file:
        data = yaml.load(file)

api_token = data['api_token']
passphrase = data['passphrase']
wallet_url = data['wallet']['url']
account_url = data['account']['url']

bitvault = helpers.bitvault()
client = bitvault.spawn()
client.context.set_token(api_token)
resources = client.resources

wallet = resources.wallet(wallet_url).get()
account = resources.account(account_url).get()

faucet_address = 'mx3Az5tkWhEQHsihFr3Nmj6mRHLeqtqfNK'

primary_seed = PassphraseBox.decrypt(passphrase, wallet.primary_private_seed)

multi_wallet = MultiWallet(
    private={'primary': primary_seed},
    public={
        'cosigner': wallet.cosigner_public_seed,
        'backup': wallet.backup_public_seed
        }
    )

unsigned_payment = account.payments.create({
    'outputs': [
        { 'amount': 6000000, 'payee': {'address': faucet_address} }
        ]
    })

#transaction = Transaction.from_data(unsigned_payment)
#change_output = transaction.outputs[-1]

#multi_wallet.is_valid_output(change_output)

#signatures = multi_wallet.signatures(transaction)




