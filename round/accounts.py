# -*- coding: utf-8 -*-
# accounts.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from coinop.bit.transaction import Transaction as CoinopTx

from .wrappers import *

import transactions as txs
import addresses


class Accounts(DictWrapper):

    def __init__(self, resource, client, wallet):
        self.wallet = wallet
        super(Accounts, self).__init__(resource, client)

    def create(self, **content):
        resource = self.resource.create(content)
        acc = self.wrap(resource)
        self.add(acc)
        return acc

    def wrap(self, resource):
        return Account(resource, self.client, self.wallet)


class Account(Wrapper, Updatable):

    def __init__(self, resource, client, wallet):
        super(Account, self).__init__(resource, client)
        self.wallet = wallet
    # Account-level rules not implemented in API.
    #    rules_resource = self.resource.rules
    #
    # @property
    # def rules(self):
    #     if not hasattr(self, '_rules'):
    #         rules_resource = self.resource.rules
    #         self._rules = Rules(rules_resource, self.client)
    #     return self._application


    def update(self, **content):
        return self.__class__(self.resource.update(content),
                              self.client,
                              wallet=self.wallet)

    def pay(self, payees):
        content = dict(outputs=self.outputs_from_payees(payees))
        unsigned = self.resource.payments.create(content)

        transaction = CoinopTx(data=unsigned.attributes)
        signatures = self.wallet.signatures(transaction)

        # TODO: investigate removing the txhash as a required param
        transaction_hash = transaction.hex_hash()
        content = dict(inputs=signatures, transaction_hash=transaction_hash)
        signed = unsigned.sign(content)
        return signed

    # Adapter for the High Level Interface to the content required by the API
    # schema.  We may change the API schema at some point to match.
    def outputs_from_payees(self, payees):
        def fn(payee):
            if 'amount' in payee and 'address' in payee:
                return dict(
                    amount=payee['amount'],
                    payee={'address': payee['address']})
            else:
                raise ValueError("Invalid payee properties")

        return map(fn, payees)

    def transactions(self, **query):
        transaction_resource = self.resource.transactions(query)
        return txs.Transactions(transaction_resource, self.client)

    @property
    def addresses(self):
        address_resource = self.resource.addresses
        return addresses.Addresses(address_resource, self.client)
