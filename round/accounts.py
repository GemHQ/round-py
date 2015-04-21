# -*- coding: utf-8 -*-
# accounts.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from coinop.bit.transaction import Transaction as CoinopTx

from .wrappers import *
from .subscriptions import Subscriptions

import transactions as txs
import addresses


class Accounts(DictWrapper):
    """A collection of round.Accounts objects.

    Args:
      resource: Account patchboard.Resource object
      client: authenticated round.Client object
      wallet: round.Wallet object to which this Account belongs.

    Returns:
      The new round.Accounts object.
    """

    def __init__(self, resource, client, wallet):
        self.wallet = wallet
        super(Accounts, self).__init__(resource, client)

    def create(self, name):
        """Create a new Account object and add it to this Accounts collection.

        Args:
          name (str): Account name

        Returns: The new round.Account
        """
        account = self.wrap(self.resource.create(dict(name=name)))
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

    def pay(self, payees, utxo_confirmations=6, mfa_token=None, redirect_uri=None):
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
          confirmations (int, optional): Required confirmations for UTXO
            selection ( > 0)
          mfa_token (str, optional): TOTP token for the Application owning this
            Account's wallet.
          redirect_uri (str, optional): URI to redirect a user to after they
            input an mfa token on the page referenced by the `mfa_uri` returned
            by this function.

        Returns: An "unapproved" Transaction with an `mfa_uri` attribute to route
          the user to the MFA confirmation page --  if called with Gem-Device
          authentication.
          An "unconfirmed" Transaction -- if called with Gem-Application auth
          (and an `mfa_token` was supplied).
        """
        # First create the unsigned tx.
        content = dict(payees=payees,
                       utxo_confirmations=utxo_confirmations)
        unsigned = self.resource.transactions().create(content)

        # Sign the tx with the primary private key.
        coinoptx = CoinopTx(data=unsigned.attributes)
        signatures = self.wallet.signatures(coinoptx)

        # Update the tx with the signatures.
        transaction = dict(signatures=dict(inputs=signatures,
                                           transaction_hash=coinoptx.hex_hash()))
        if redirect_uri:
            transaction[u'redirect_uri'] = redirect_uri

        signed = txs.Transaction(unsigned.update(transaction), self.client)

        # If this is an Application wallet, approve the transaction.
        if mfa_token and self.wallet.application:
            return txs.Transaction(signed.with_mfa(mfa_token).approve())

        # Otherwise return the unapproved tx (now redirect the user to the
        # `mfa_uri` attribute to approve!)
        return signed

    def transactions(self, **query):
        """Fetch and return Transactions involving any Address inside this
        Account.

        Args:
          status (str or list, optional): One or a list of
            ["unsigned", "unapproved",
             "confirmed", "unconfirmed",
             "canceled", "denied"]
          type (str, optional): One of ["incoming", "outgoing"]

        Returns:
          A collection of matching Transactions
        """
        if u'status' in query and isinstance(query[u'status'], list):
            query[u'status'] = ','.join(map(str, query[u'status']))

        transaction_resource = self.resource.transactions(query)
        return txs.Transactions(transaction_resource, self.client)

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions registered on this account."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions

    @property
    def addresses(self):
        """Fetch and return Addresses inside this Account."""
        address_resource = self.resource.addresses
        return addresses.Addresses(address_resource, self.client)
