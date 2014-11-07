# -*- coding: utf-8 -*-
# wallets.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

from .wrappers import *
from .accounts import Account, Accounts
from .rules import Rule, Rules

# The passphrase parameter should stay out of the content dict
# so that there is no chance the client's passphrase will get passed
# to our server.
def generate(passphrase, network=DEFAULT_NETWORK, **content):
    multi_wallet = MultiWallet.generate([u'primary', u'backup'], network=network)

    primary_seed = multi_wallet.private_seed(u'primary')
    backup_seed = multi_wallet.private_seed(u'backup')

    primary_public_seed = multi_wallet.public_seed(u'primary')
    backup_public_seed = multi_wallet.public_seed(u'backup')

    encrypted_seed = PassphraseBox.encrypt(passphrase, primary_seed)

    content[u'network'] = GEM_NETWORK[network]
    content[u'backup_public_seed'] = backup_public_seed
    content[u'primary_public_seed'] = primary_public_seed
    content[u'primary_private_seed'] = encrypted_seed
    return backup_seed, content


class Wallets(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        wallet = self.wrap(resource)
        self.add(wallet)
        return wallet

    def wrap(self, resource):
        return Wallet(resource, self.client)


class Wallet(Wrapper, Updatable):

    def __init__(self, resource, client):
        super(Wallet, self).__init__(resource, client)

        self.multi_wallet = None

        account_resource = self.resource.accounts
        self.accounts = Accounts(resource=account_resource,
                                 client=self.client,
                                 wallet=self)

    @property
    def rules(self):
        if not hasattr(self, '_rules'):
            rules_resource = self.resource.rules
            self._rules = Rules(rules_resource,
                                self.client)
        return self._application

    def is_unlocked(self):
        return not self.is_locked()

    def is_locked(self):
        return (self.multi_wallet is None)

    def unlock(self, passphrase, network=None):
        network = network if network else self.resource.network
        wallet = self.resource
        primary_seed = PassphraseBox.decrypt(
            passphrase,
            wallet.primary_private_seed)

        self.multi_wallet = MultiWallet(
            private={u'primary': primary_seed},
            public={
                u'cosigner': wallet.cosigner_public_seed,
                u'backup': wallet.backup_public_seed},
            network=NETWORK_MAP[network])

    def signatures(self, transaction):
        # TODO: output.metadata['type']['change']
        change_output = transaction.outputs[-1]
        if self.multi_wallet.is_valid_output(change_output):
            return self.multi_wallet.signatures(transaction)
        else:
            raise Exception('Problem with transaction: Invalid change address')
