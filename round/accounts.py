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

    def __init__(self, resource, client, wallet):
        """
        Initialize a round.Accounts from an Accounts patchboard.Resource object.
        Return the new round.Accounts object.
        Keyword arguments:
        resource --  Account patchboard.Resource object
        client -- authenticated round.Client object
        wallet -- round.Wallet object to which this Account belongs.
        """
        self.wallet = wallet
        super(Accounts, self).__init__(resource, client)

    def create(self, **content):
        """
        Create a new Account object and add it to this Accounts collection.
        Return the new round.Account.
        Keyword arguments:
        name -- Account name
        """
        resource = self.resource.create(content)
        acc = self.wrap(resource)
        self.add(acc)
        return acc

    def wrap(self, resource):
        """
        Return a round.Account constructed from a patchboard.Resource object.
        Keyword arguments:
        resource -- Account patchboard.Resource object
        """
        return Account(resource, self.client, self.wallet)


class Account(Wrapper, Updatable):

    def __init__(self, resource, client, wallet):
        """
        Initialize a round.Account from an Account patchboard.Resource object.
        Return the new round.Account object.
        Keyword arguments:
        resource --  Account patchboard.Resource object
        client -- authenticated round.Client object
        wallet -- round.Wallet object to which this Account belongs.
        """
        super(Account, self).__init__(resource, client)
        self.wallet = wallet

    def update(self, **kwargs):
        """
        Update the Account resource with specified content.
        Return the updated Account object.
        Keyword arguments:
        name -- name for the account
        """
        return self.__class__(self.resource.update(kwargs),
                              self.client,
                              wallet=self.wallet)

    def pay(self, payees, confirmations=6):
        """
        Create an unsigned transaction.
        Verify and sign the transaction, then submit the signed tx to the server
        for signing and publication.
        Return the unconfirmed Transaction.
        Keyword arguments:
        payees -- list of outputs in the form: [{'amount': 10000(satoshis),
                                                 'address':'validbtcaddress'}, ...]
        confirmations -- Required confirmations for UTXO selection (integer > 1)
        """
        content = dict(outputs=self.outputs_from_payees(payees), confirmations=confirmations)
        unsigned = self.resource.payments.create(content)

        transaction = CoinopTx(data=unsigned.attributes)
        signatures = self.wallet.signatures(transaction)

        # TODO: investigate removing the txhash as a required param
        transaction_hash = transaction.hex_hash()
        content = dict(inputs=signatures, transaction_hash=transaction_hash)
        signed = unsigned.sign(content)
        return txs.Transaction(signed, self.client)

    def outputs_from_payees(self, payees):
        """
        Adapt the payees parameter from the high level interface and return the
        format required by the API schema. We may change the API schema at some
        point to match.
        Keyword arguments:
        payees -- [{'amount': 10000(satoshis), 'address':'validbtcaddress'}, ...]
        Return:
                  [{'amount': 10000, 'payee': {'address': 'validbtcaddress'}, ...]
        """
        def fn(payee):
            if 'amount' in payee and 'address' in payee:
                return dict(
                    amount=payee['amount'],
                    payee={'address': payee['address']})
            else:
                raise ValueError("Invalid payee properties")

        return map(fn, payees)

    def transactions(self, **query):
        """
        Fetch and return Transactions involving any Address inside this Account.
        Keyword arguments:
        status -- One of "confirmed", "unconfirmed", "unsigned", "canceled"
        type -- One of "incoming", "outgoing"
        """
        transaction_resource = self.resource.transactions(query)
        return txs.Transactions(transaction_resource, self.client)

    @property
    def subscriptions(self):
        """
        Fetch and return Subscriptions associated with this account.
        """
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions

    @property
    def addresses(self):
        """
        Fetch and return Addresses inside this Account.
        """
        address_resource = self.resource.addresses
        return addresses.Addresses(address_resource, self.client)
