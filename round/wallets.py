# -*- coding: utf-8 -*-
# wallets.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from coinop.passphrasebox import PassphraseBox
from coinop.crypto.passphrasebox import PassphraseBox as NaclPassphraseBox

from coinop.multiwallet import MultiWallet

from .wrappers import *
from .errors import *
from .accounts import Account, Accounts
from .subscriptions import Subscription, Subscriptions

def generate(passphrase, trees=['primary']):
    """Generate a seed for the primary tree of a Gem wallet.

    You may choose to store the passphrase for a user so the user doesn't have
    to type it in every time. This is okay (although the security risks should
    be obvious) but Gem strongly discourages storing even the encrypted private
    seed, and storing both the passphrase and the private seed is completely
    insane. Don't do it.

    Args:
      passphrase (str): The passphrase that will be used to encrypt the seed
        before it's send to Gem. Key-stretching is done with PBDKF2 and
        encryption is done with nacl's SecretBox.
      trees (list of str): A list of names to generate trees for. For User
        Wallets this will be ['primary'], for Application Wallets it will be
       ['primary', 'backup'].

    Returns:
      A dict of dicts containing the serialized public master node, and
       a sub-dict with the encrypted private seed for each tree in `trees`.
    """
    seeds, multi_wallet = MultiWallet.generate(trees, entropy=True)

    result = {}
    for tree in trees:
        result[tree] = dict(private_seed=seeds[tree],
                            public_seed=multi_wallet.public_wif(tree),
                            encrypted_seed=NaclPassphraseBox.encrypt(passphrase,
                                                                     seeds[tree]))
    return result


class Wallets(DictWrapper):
    """A collection of round.Wallets objects."""

    def __init__(self, resource, client, application=False):
        # This is less than awesome. Ideally a PB resource can learn whether it's
        # an application_wallets or user_wallets object.
        self.application = application
        super(Wallets, self).__init__(resource, client)

    def create(self, name, passphrase=None, wallet_data=None):
        """Create a new Wallet object and add it to this Wallets collection.
        This is only available in this library for Application wallets. Users
        must add additional wallets in their User Console

        Args:
          name (str): wallet name
          passphrase (str, optional): A passphrase with which to encrypt a user
            wallet. If not supplied, wallet_data is mandatory.
          wallet_data (dict): Output from wallets.generate.
            For User Wallets, only the primary tree is used.
            For Application Wallets, the primary and backup trees are used.

        Returns:
          A tuple of the (backup_private_seed, round.Wallet).
        """
        if not self.application:
            raise RoundError("User accounts are limited to one wallet. Make an "
                             "account or shoot us an email <dev@gem.co> if you "
                             "have a compelling use case for more.")
        if not passphrase and not wallet_data:
            raise ValueError("Usage: wallets.create(name, passphrase [, "
                             "wallet_data])")
        elif passphrase:
            wallet_data = generate(passphrase,
                                   trees=(['primary', 'backup'] if (
                                       self.application) else ['primary']))

        wallet = dict(
            primary_private_seed=wallet_data['primary']['encrypted_seed'],
            primary_public_seed=wallet_data['primary']['public_seed'],
            name=name)
        if self.application:
            wallet['backup_public_seed'] = wallet_data['backup']['public_seed']

        resource = self.resource.create(wallet)
        wallet = self.wrap(resource)
        return (wallet_data['backup']['private_seed'], self.add(wallet)) if (
            self.application) else self.add(wallet)

    def wrap(self, resource):
        return Wallet(resource, self.client, self.application)


class Wallet(Wrapper, Updatable):
    """A Gem Wallet represents a 3-key multisig HD bitcoin wallet.

    Attributes:
      primary_private_seed (dict): An encrypted representation of the private
        seed for the primary tree. This is encrypted with a user-chosen
        passphrase that is never sent to Gem. This is used for signing
        transactions within this client libary.
      primary_public_seed (str): A misnomer, this is the serialized master node
        of the primary tree.
      backup_public_seed (str): A misnomer, this is the serialized master node
        of the backup tree. The backup private seed is generated out-of-band by
        the end user when they confirm their email address and MFA information.
        In the case of an Application wallet, the backup public can be delivered
        in-band during the wallets.create call.
      cosigner_public_seed (str): A misnomer, this is the serialized master node
        of the cosigner tree. The cosigner private seed is generated and held by
        Gem in Hardware Security Modules.
      name (str): A human-readable name for the wallet. A User's primary wallet
        is named 'default'.
      multi_wallet (coinop.Transaction): When unlocked, this variable will be
        populated with a high-level interface wrapper around the primary private
        seed.

    Args:
      resource (patchboard.Resource): server-side Wallet object
      client (round.Client)
    """

    def __init__(self, resource, client, application=None):
        super(Wallet, self).__init__(resource, client)

        self.application = application
        self.multi_wallet = None

        account_resource = self.resource.accounts
        self.accounts = Accounts(resource=account_resource,
                                 client=self.client,
                                 wallet=self)
    @property
    def default_account(self):
        return self.accounts['default']

    def is_unlocked(self):
        """Return true if the wallet is unlocked."""
        return not self.is_locked()

    def is_locked(self):
        """Return true if the wallet is locked."""
        return (self.multi_wallet is None)

    def unlock(self, passphrase):
        """Unlock the Wallet by decrypting the primary_private_seed with the
        supplied passphrase. Once unlocked, the private seed is accessible in
        memory and calls to `account.pay` will succeed. This is a necessary step
        for creating transactions.

        Args:
          passphrase (str): The passphrase the User used to encrypt this wallet.
        Returns:
          self
        """
        wallet = self.resource
        try:
            if wallet.primary_private_seed['nonce']:
                primary_seed = NaclPassphraseBox.decrypt(
                    passphrase, wallet.primary_private_seed)
            else:
                primary_seed = PassphraseBox.decrypt(
                    passphrase, wallet.primary_private_seed)
        except:
            raise InvalidPassphraseError()

        self.multi_wallet = MultiWallet(
            private_seeds={'primary': primary_seed},
            public={'cosigner': wallet.cosigner_public_seed,
                    'backup': wallet.backup_public_seed})
        return self

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions associated with this wallet."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions

    def signatures(self, transaction):
        """Sign a transaction.

        Args:
          transaction (coinop.Transaction)

        Returns:
          A list of signature dicts of the form
            [ {'primary': 'base58signaturestring'},
              ... ]
        """
        # TODO: output.metadata['type']['change']
        if not self.multi_wallet:
            raise DecryptionError("This wallet must be unlocked with "
                                  "wallet.unlock(passphrase)")

        return self.multi_wallet.signatures(transaction)
