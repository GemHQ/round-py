# -*- coding: utf-8 -*-
# accounts.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

import logging
from .config import *
from .errors import *
from patchboard.response import ResponseError

from coinop.transaction import Transaction as CoinopTx

from .wrappers import *
from .subscriptions import Subscriptions
from .addresses import Addresses
from .netki import NetkiNames
from .transactions import Transaction, Transactions

logger = logging.getLogger(__name__)

class Accounts(DictWrapper):
    """A collection of round.Accounts objects.

    Args:
      resource: Account patchboard.Resource object
      client: authenticated round.Client object
      wallet: round.Wallet object to which this Account belongs.

    Returns:
      The new round.Accounts object.
    """

    def __init__(self, resource, client, wallet=None, populate=False):
        self.wallet = wallet
        super(Accounts, self).__init__(resource, client, populate)

    def __getitem__(self, name):
        if name in self._data: return self._data.__getitem__(name)
        try:
            account = self.wrap(
                self.wallet.resource.account_query(dict(name=name)).get())
            self.add(account)
            return account
        except (RoundError, ResponseError) as e:
            logger.debug(e)
            raise KeyError(name)

    def create(self, name, network):
        """Create a new Account object and add it to this Accounts collection.

        Args:
          name (str): Account name
          network (str): Type of cryptocurrency.  Can be one of, 'bitcoin', '
            bitcoin_testnet', 'litecoin', 'dogecoin'.

        Returns: The new round.Account
        """
        if not network in SUPPORTED_NETWORKS:
            raise ValueError('Network not valid!')
        account = self.wrap(self.resource.create(dict(name=name,
                                                      network=network)))
        self.add(account)
        return account

    def wrap(self, resource):
        return Account(resource, self.client, self.wallet)


class Account(Wrapper, Updatable):
    """Accounts contain a sub-tree of a Wallet. (m/44/0/_)

    Attributes:
      addresses (round.Addresses): Collection of Addresses owned by this Account.
      subscriptions (round.Subscriptuions): Collection of Subscriptions
        registered on this Account.

    Args:
      resource (patchboard.Resource): server-side Account object
      client (round.Client)
      wallet (round.Wallet): The Wallet to which this Account belongs
    """

    def __init__(self, resource, client, wallet):
        super(Account, self).__init__(resource, client)
        self.wallet = wallet

    def update(self, **kwargs):
        """Update the Account resource with specified content.

        Args:
          name (str): Human-readable name for the account

        Returns: the updated Account object.
        """
        return self.__class__(self.resource.update(kwargs),
                              self.client,
                              wallet=self.wallet)

    def pay(self, payees, change_account=None, utxo_confirmations=6,
            mfa_token=None, redirect_uri=None):
        """Create, verify, and sign a new Transaction.

        If this Account is owned by a User object, the user must be redirected to
        a URL (`mfa_uri`) returned by this call to input their MFA token. After
        they complete that step, the Transaction will be approved and published
        to the bitcoin network. If a `redirect_uri` is provided in this call, the
        user will be redirected to that uri after they complete the MFA challenge
        so it's a good idea to have an endpoint in your app (or custom scheme on
        mobile) that can provide the user a seamless flow for returning to your
        application. If they have not configured a TOTP MFA application (e.g.
        Google Authenticator), then an SMS will be sent to their phone number
        with their token.

        If this Account is owned by an Application, the `mfa_token` can be
        included in this call and the Transaction will be automatically approved
        and published to the blockchain.

        Args:
          payees (list of dict): list of outputs in the form:
            [{'amount': 10000(satoshis),
              'address':'validbtcaddress'}, ...]
          change_account (str or Account): if supplied, this account will
            be used to generate a change address in the event that a change
            output is required. This account must be owned by the same Wallet.
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
        if self.wallet.is_locked():
            raise DecryptionError("This wallet must be unlocked with "
                                  "wallet.unlock(passphrase)")

        # First create the unsigned tx.
        content = dict(payees=payees,
                       utxo_confirmations=utxo_confirmations,
                       remainder_account=self.resource.attributes['key'],
                       network=self.network)

        if change_account: content['change_account'] = \
           self.wallet._get_account_attr(change_account)

        try:
            unsigned = self.resource.transactions().create(content)
        except ResponseError as e:
            if "cannot cover" in e.message:
                raise BalanceError(e.message)
            raise e

        # Sign the tx with the primary private key.
        coinoptx = CoinopTx(data=unsigned.attributes)
        signatures = self.wallet.signatures(coinoptx)

        # Update the tx with the signatures.
        transaction = dict(signatures=dict(inputs=signatures,
                                           transaction_hash=coinoptx.hash))
        if redirect_uri:
            transaction['redirect_uri'] = redirect_uri

        signed = Transaction(unsigned.update(transaction), self.client)

        # If this is an Application wallet, approve the transaction.
        if mfa_token and self.wallet.application:
            try:
                return Transaction(signed.with_mfa(mfa_token).approve(),
                                   self.client)
            except Exception as e:
                signed = signed.cancel()
                logger.debug(e.message)
                logger.debug("If you are having trouble with MFA tokens, make "
                             "sure your system time is accurate with `date -u`!")

        # Otherwise return the unapproved tx (now redirect the user to the
        # `mfa_uri` attribute to approve!)
        return signed

    def balances_at(self, utxo_confirmations=6):
        """Return the confirmed, claimed (reserved for a pending, unsigned
        transaction), and available balances, where the threshold for
        confirmed is the value of `utxo_confirmations`.

        Args:
          utxo_confirmations (int): the # of confirmations to use when computing
            balances.

        Returns:
          A dict of form { u'available_balance': 0,
                           u'claimed_balance': 0,
                           u'confirmed_balance': 0,
                           u'utxo_confirmations': 0 }
        """
        return self.resource.available(
            {'utxo_confirmations': utxo_confirmations}).__dict__['data']

    def transactions(self, **query):
        """Fetch and return Transactions involving any Address inside this
        Account.
        Note that this call is not cached. If you want to store a copy, you
        must assign it to a local variable, and call .refresh() when you need
        updated data

        Args:
          status (str or list, optional): One or a list of
            ["unsigned", "unapproved",
             "confirmed", "unconfirmed",
             "canceled", "denied"]
          type (str, optional): One of ["incoming", "outgoing"]

        Returns:
          A collection of matching Transactions
        """
        if 'status' in query and isinstance(query['status'], list):
            query['status'] = ','.join(map(str, query['status']))

        transaction_resource = self.resource.transactions(query)
        return Transactions(transaction_resource, self.client, populate=True)

    @property
    @cacheable
    def subscriptions(self):
        """Return the cached Subscriptions object for this Account."""
        return self.get_subscriptions()

    def get_subscriptions(self, fetch=False):
        """Return this Account's subscriptions object, populating it if fetch is True."""
        return Subscriptions(
            self.resource.subscriptions, self.client, populate=fetch)

    @property
    @cacheable
    def addresses(self):
        """Fetch and return an updted list of Addresses inside this Account."""
        return self.get_addresses()

    def get_addresses(self, fetch=False):
        """Return the Account's addresses object, populating it if fetch is True."""
        return Addresses(self.resource.addresses, self.client, populate=fetch)

    @property
    @cacheable
    def netki_names(self):
        """Fetch and return an updated list of NetkiNames inside this Account."""
        return self.get_netki_names()

    def get_netki_names(self, fetch=False):
        """Return the Account's NetkiNames object, populating it if fetch is True."""
        return NetkiNames(self.resource.netki_names, self.client, populate=fetch)
