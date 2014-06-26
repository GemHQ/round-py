# wrappers.py
#
# Copyright 2014 BitVault.


from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

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

        accounts_resource = self.resource.accounts
        self.accounts = bitvault.collections.Accounts(accounts_resource)

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

    def addresses(self):
        pass

    def pay(self, payees):
        # HOPEFUL
        unsigned = foo()
        transaction = Transaction.from_data(unsigned)
        change_output = transaction.outputs[-1]
        multi_wallet.is_valid_output(change_output)
        signatures = multi_wallet.signatures(transaction)
        signed = sign(signatures)
        return signed

    def transactions(self):
        pass

