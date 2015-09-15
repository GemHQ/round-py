# -*- coding: utf-8 -*-
# wallets.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals
from future.utils import iteritems
import logging

from .config import *

from coinop.passphrasebox import PassphraseBox
from coinop.crypto.passphrasebox import PassphraseBox as NaclPassphraseBox

from coinop.multiwallet import MultiWallet
from coinop.transaction import Transaction as CoinopTx

from .wrappers import *
from .errors import *
from .accounts import Account, Accounts
from .subscriptions import Subscription, Subscriptions
import round.transactions as txs

logger = logging.getLogger(__name__)

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
                            encrypted_seed=PassphraseBox.encrypt(passphrase,
                                                                 seeds[tree]))
    return result


class Wallets(DictWrapper):
    """A collection of round.Wallets objects."""

    def __init__(self, resource, client, populate=False, application=False):
        # This is less than awesome. Ideally a PB resource can learn whether it's
        # an application_wallets or user_wallets object.
        self.application = application
        super(Wallets, self).__init__(resource, client, populate)

    def __getitem__(self, name):
        if name in self._data: return self._data.__getitem__(name)
        try:
            wallet = self.wrap(
                self.application.resource.wallet_query(dict(name=name)).get())
            self.add(wallet)
            return wallet
        except Exception as e:
            logger.debug(e)
            raise KeyError(name)

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

    def is_unlocked(self):
        """Return true if the wallet is unlocked."""
        return not self.is_locked()

    def is_locked(self):
        """Return true if the wallet is locked."""
        return (self.multi_wallet is None)

    def unlock(self, passphrase, encrypted_seed=None):
        """Unlock the Wallet by decrypting the primary_private_seed with the
        supplied passphrase. Once unlocked, the private seed is accessible in
        memory and calls to `account.pay` will succeed. This is a necessary step
        for creating transactions.

        Args:
          passphrase (str): The passphrase the User used to encrypt this wallet.
          encrypted_seed (dict): A dictionary of the form
            {'ciphertext': longhexvalue,
             'iterations': integer of pbkdf2 derivations,
             'nonce': 24-byte hex value
             'salt': 16-byte hex value}
            this dict represents an private seed (not a master key) encrypted
            with the `passphrase` using pbkdf2. You can obtain this value with
            wallet.generate. If this value is supplied, it overwrites (locally
            only) the encrypted primary_private_seed value, allowing you to load
            in a primary key that you didn't store with Gem. Note that the key
            MUST match the pubkey that this wallet was created with.
        Returns:
          self
        """
        wallet = self.resource
        if not encrypted_seed:
            encrypted_seed = wallet.primary_private_seed
        try:
            if encrypted_seed['nonce']:
                primary_seed = NaclPassphraseBox.decrypt(
                    passphrase, encrypted_seed)
            else:
                primary_seed = PassphraseBox.decrypt(
                    passphrase, encrypted_seed)
        except:
            raise InvalidPassphraseError()

        self.multi_wallet = MultiWallet(
            private_seeds={'primary': primary_seed},
            public={'cosigner': wallet.cosigner_public_seed,
                    'backup': wallet.backup_public_seed})
        return self

    def balances_at(self, utxo_confirmations=6, network=None):
        """Return the confirmed, claimed (reserved for a pending, unsigned
        transaction), and available balances, where the threshold for
        confirmed is the value of `utxo_confirmations`.

        Args:
          utxo_confirmations (int): the # of confirmations to use when computing
            balances.
          network (str): Type of cryptocurrency.  Can be one of, 'bitcoin', '
            bitcoin_testnet', 'litecoin', 'dogecoin'.

        Returns:
          A dict of form { u'available_balance': 0,
                           u'claimed_balance': 0,
                           u'confirmed_balance': 0,
                           u'utxo_confirmations': 0 }
        """
        if not network in SUPPORTED_NETWORKS:
            raise ValueError('Network not valid!')
        return self.resource.available({'utxo_confirmations': utxo_confirmations,
                                        'network': network}).__dict__['data']

    @property
    @cacheable
    def accounts(self):
        """Return the cached Accounts object for this Wallet."""
        return self.get_accounts()

    def get_accounts(self, fetch=False):
        """Return this Wallet's accounts object, populating it if fetch is True."""
        return Accounts(self.resource.accounts, self.client, wallet=self, populate=fetch)

    @property
    def default_account(self):
        return self.accounts['default']

    def account(self, key=None, address=None, name=None):
        """Query for an account by key, address, or name."""
        if key:
            return self.client.account(key, wallet=self)
        if address:
            q = dict(address=address)
        elif name:
            q = dict(name=name)
        else:
            raise TypeError("Missing param: key, address, or name is required.")

        return Account(
            self.resource.account_query(q).get(), self.client, wallet=self)

    def dump_addresses(self, network, filename=None):
        """Return a list of address dictionaries for each address in all of the
        accounts in this wallet of the network specified by `network`
        """
        addrs =  [addr.data for a in self.accounts.values() if a.network == network
                            for addr in a.addresses]
        if filename:
            from json import dump
            with open(filename, 'w') as f:
                dump(addrs, f)

        return addrs

    @property
    @cacheable
    def subscriptions(self):
        """Return the cached Subscriptions object for this Wallet."""
        return self.get_subscriptions()

    def get_subscriptions(self, fetch=False):
        """Return this Wallet's subscriptions object, populating it if fetch is True."""
        return Subscriptions(
            self.resource.subscriptions, self.client, populate=fetch)


    def _get_account_attr(self, obj, attr='key'):
        try:
            return obj.resource.attributes[attr]
        except AttributeError:
            return self.accounts[obj].resource.attributes[attr]

    def pay(self, payees, remainder_account, payers=None, change_account=None,
            network=None, utxo_confirmations=6, mfa_token=None, redirect_uri=None):
        """Create, verify, and sign a new Transaction.

        This method is distinct from Account.pay in that it exposes the `payers`
        parameter which allows you to create transactions using inputs from
        multiple Accounts (which must ALL belong to this Wallet) by specifying
        a dict with account names or Account objects and amounts to be deducted.

        Note that a change output will be created for each account if necessary
        to deduct the precise amount specified. Fees will be drawn from the
        `remainder_account`, as well as any difference between the sum of `payee`
        outputs and the `payers` inputs. (Which is why `remainder_account` is
        mandatory and `payers` is optional.)

        If this Wallet is owned by a User object, the user must be redirected to
        a URL (`mfa_uri`) returned by this call to input their MFA token. After
        they complete that step, the Transaction will be approved and published
        to the bitcoin network. If a `redirect_uri` is provided in this call, the
        user will be redirected to that uri after they complete the MFA challenge
        so it's a good idea to have an endpoint in your app (or custom scheme on
        mobile) that can provide the user a seamless flow for returning to your
        application. If they have not configured a TOTP MFA application (e.g.
        Google Authenticator), then an SMS will be sent to their phone number
        with their token.

        If this Wallet is owned by an Application, the `mfa_token` can be
        included in this call and the Transaction will be automatically approved
        and published to the blockchain.

        ********************************* NOTE *********************************

        Additionally, if your use-case does not require keeping precise values
        in your Accounts, you may want to create a transaction without limiting
        your UTXO selection to specific Accounts.

        To do this, you must explicitly pass in `None` as the value for
        `remainder_account` and omit the `payers` parameter. This is to prevent
        accidental spends out of incorrect accounts.

        ************************************************************************

        Args:
          payees (list of dict): list of outputs in the form:
            [{'amount': 10000(satoshis),
              'address':'validbtcaddress'}, ...]
          remainder_account (str or Account or None): an Account to handle the
            difference between payer and payee sums as well as tx fees
            (if set to None, a transaction will be created that potentially
             uses UTXOs from every Account belonging to this wallet)
          payers (list of dict, optional): list of input accounts in the form:
            [{'amount': 10000(satoshis),
              'account': ('accountname'||accountInstance)}, ...]
          change_account (str or Account): if supplied, this account will
            be used to generate a change address in the event that a change
            output is required. Note that this does not replace the change
            outputs that will be generated to ensure that each Account in
            `payers` (if supplied) is deducted the precise amounts specified.
          network (str): Type of cryptocurrency.  Can be one of, 'bitcoin', '
            bitcoin_testnet', 'litecoin', 'dogecoin'.
          utxo_confirmations (int, optional): Required confirmations for UTXO
            selection ( > 0)
          mfa_token (str/function, optional): TOTP token for the Application
            owning this Account's wallet OR a callable/function which will
            generate such a token. The latter is suggested
            (e.g. application.get_mfa) as otherwise, the token might be
            invalidated by the time tx.create and tx.update complete (before
            the tx.approve call which actually requires the mfa_token).
          redirect_uri (str, optional): URI to redirect a user to after they
            input an mfa token on the page referenced by the `mfa_uri` returned
            by this function.

        Returns: An "unapproved" Transaction with an `mfa_uri` attribute to route
          the user to the MFA confirmation page --  if called with Gem-Device
          authentication.
          An "unconfirmed" Transaction -- if called with Gem-Application auth
          (and an `mfa_token` was supplied).
        """
        # Check that wallet is unlocked
        if self.is_locked():
            raise DecryptionError("This wallet must be unlocked with "
                                  "wallet.unlock(passphrase)")

        # First create the unsigned tx.
        content = dict(payees=payees,
                       utxo_confirmations=utxo_confirmations,
                       network=network)

        if remainder_account is not None:
            if payers: raise TypeError(
                    "Invalid payers: either supply a remainder_account "
                    "or omit the payers parameter")
            content['network'] = self._get_account_attr(
                remainder_account, 'network')
            content['remainer_account'] = self._get_account_attr(
                remainder_account, 'key')

        elif not payers and not network:
            raise TypeError("Missing network: network is required if "
                            "remainder_account is not specified")

        if change_account:
            content['change_account'] = self._get_account_attr(change_account)

        if payers: content['payers'] = [
            dict(p, account=self._get_account_attr(p['account'])) for p in payers
        ]

        try:
            unsigned = self.resource.transactions().create(content)
        except ResponseError as e:
            if "cannot cover" in e.message:
                raise BalanceError(e.message)
            raise e

        # Sign the tx with the primary private key.
        coinoptx = CoinopTx(data=unsigned.attributes)
        signatures = self.signatures(coinoptx)

        # Update the tx with the signatures.
        transaction = dict(signatures=dict(inputs=signatures,
                                           transaction_hash=coinoptx.hash))
        if redirect_uri:
            transaction['redirect_uri'] = redirect_uri

        signed = txs.Transaction(unsigned.update(transaction), self.client)

        # If this is an Application wallet, approve the transaction.
        if mfa_token and self.application:
            if hasattr(mfa_token, '__call__'): # callable() is unsupported by 3.1 and 3.2
                mfa_token = mfa_token.__call__()
            try:
                return txs.Transaction(signed.with_mfa(mfa_token).approve(),
                                       self.client)
            except Exception as e:
                signed.cancel()
                logger.debug(e.message)
                logger.debug("If you are having trouble with MFA tokens, make "
                             "sure your system time is accurate with `date -u`!")

        # Otherwise return the unapproved tx (now redirect the user to the
        # `mfa_uri` attribute to approve!)
        return signed

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
