# wrappers.py
#
# Copyright 2014 BitVault.


from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet
from coinop.bit.transaction import Transaction

import bitvault


class Wrapper(object):

    def __init__(self, resource):
        self.resource = resource

    def __getattr__(self, name):
        # TODO: may want to limit the delegation to specific attrs.
        return getattr(self.resource, name)


class User(Wrapper):

    def __init__(self, resource):
        super(User, self).__init__(resource)
        app_resource = self.resource.applications
        self.applications = bitvault.collections.Applications(app_resource)


class Application(Wrapper):

    def __init__(self, resource):
        super(Application, self).__init__(resource)
        wallets_resource = self.resource.wallets
        self.wallets = bitvault.collections.Wallets(wallets_resource)


class Wallet(Wrapper):

    def __init__(self, resource):
        super(Wallet, self).__init__(resource)

        self.multi_wallet = None
        ar = self.resource.accounts
        self.accounts = bitvault.collections.Accounts(resource=ar, wallet=self)

    def is_unlocked(self):
        return not self.is_locked()

    def is_locked(self):
        return (self.multi_wallet is None)

    def unlock(self, passphrase):
        wallet = self.resource
        primary_seed = PassphraseBox.decrypt(
            passphrase,
            wallet.primary_private_seed)

        self.multi_wallet = MultiWallet(
            private={u'primary': primary_seed},
            public={
                u'cosigner': wallet.cosigner_public_seed,
                u'backup': wallet.backup_public_seed})


    def transfer(self, options):
        pass

class Account(Wrapper):

    def __init__(self, resource, wallet):
        super(Account, self).__init__(resource)
        self.wallet = wallet


    def pay(self, payees):
        multi_wallet = self.wallet.multi_wallet
        content = dict(outputs=self.outputs_from_payees(payees))
        unsigned = self.resource.payments.create(content)

        transaction = Transaction(data=unsigned.attributes)
        change_output = transaction.outputs[-1]

        if multi_wallet.is_valid_output(change_output):
            signatures = multi_wallet.signatures(transaction)
        else:
            raise Exception('Problem with transaction: Invalid change address')

        transaction_hash = transaction.hex_hash()
        content = dict(inputs=signatures, transaction_hash=transaction_hash)
        #print repr(content)
        signed = unsigned.sign(content)
        return signed

    def outputs_from_payees(self, payees):
        def fn(payee):
            if 'amount' in payee and 'address' in payee:
                return dict(amount=payee['amount'],
                        payee={'address': payee['address']})
            else:
                raise ValueError("Invalid payee properties")

        return map(fn, payees)

    def transactions(self):
        pass

