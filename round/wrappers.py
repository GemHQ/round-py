# -*- coding: utf-8 -*-
# wrappers.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pprint import pprint as pp
from .config import *
from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet
from coinop.bit.transaction import Transaction as Tx
from patchboard.response import ResponseError

import dict_wrappers
import list_wrappers

class Updatable(object):

    def update(self, **content):
        return self.__class__(self.resource.update(content),
                              self.client)


class Wrapper(object):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client

    def __getattr__(self, name):
        return getattr(self.resource, name)

    def __str__(self):
        return str(self.attributes)

    def refresh(self):
        self.resource = self.resource.get()
        return self


class Developers(object):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client

    def create(self, **content):
        priv = content[u'privkey'] if u'privkey' in content else None
        resource = self.resource.create(content)
        if priv:
            resource.context.authorize(u'Gem-Developer',
                                       email=content[u'email'],
                                       privkey=priv)
        return self.wrap(resource)

    def wrap(self, resource):
        return Developer(resource, self.client)


class Developer(Wrapper):

    def update(self, **content):
        resource = self.resource.update(content)

        email = resource.attributes.get(u'email', None)
        priv = content.get(u'privkey', None)

        resource.context.authorize(u'Gem-Developer',
                                   email=email,
                                   privkey=priv)
        return Developer(resource, self.client)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            apps_resource = self.resource.applications
            self._applications = dict_wrappers.Applications(apps_resource,
                                                            self.client)
        return self._applications


class User(Wrapper, Updatable):

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource, self.client)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            apps_resource = self.resource.applications
            self._applications = dict_wrappers.Applications(apps_resource,
                                                            self.client)
        return self._applications

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = dict_wrappers.Wallets(wallets_resource,
                                                  self.client)
        return self._wallets

    def authorize_device(self, **content):
        try:
            reply = self.resource.authorize_device(content)
            # Doesn't require the app_url, since that is only for the
            # client.application convenience method.
            self.resource.context.authorize(scheme='Gem-Device',
                                            api_token=self.context.api_token,
                                            user_url=self.url,
                                            user_token=self.user_token,
                                            device_id=content['device_id'])
            return self
        except ResponseError as e:
            try:
                reply = e.headers[u'WWW-Authenticate']
            except:
                raise e
        return reply


class Rule(Wrapper):

    def set(self, content):
        for name, spec in content.iteritems():
            if spec[u'type'] in [u'wallet', u'account']:
                resource = spec[u'value']
                spec[u'value'] = dict(url=resource[u'url'])
        return self.resource.set(content)

    def delete(self):
        return self.resource.delete.response.data


class Application(Wrapper, Updatable):

    @property
    def users(self):
        if not hasattr(self, u'_users'):
            users_resource = self.resource.users
            self._users = dict_wrappers.Users(users_resource,
                                              self.client)
        return self._users

    @property
    def rules(self):
        if not hasattr(self, u'_rules'):
            rules_resource = self.resource.rules
            self._rules = dict_wrappers.Rules(rules_resource,
                                              self.client)
        return self._rules

    def authorize_instance(self, **content):
        if (not hasattr(self, u'_application_instance') or
            not self._application_instance):
            self._application_instance = self.resource.authorize_instance(content)
            if self._application_instance:
                self.context.authorize(u'Gem-Application',
                                       api_token=self.api_token,
                                       instance_id=self._instance_id)
        return self._application_instance

class Wallet(Wrapper, Updatable):

    def __init__(self, resource, client):
        super(Wallet, self).__init__(resource, client)

        self.multi_wallet = None

        account_resource = self.resource.accounts
        self.accounts = dict_wrappers.Accounts(resource=account_resource,
                                               client=self.client,
                                               wallet=self)

    @property
    def rules(self):
        if not hasattr(self, '_rules'):
            rules_resource = self.resource.rules
            self._rules = dict_wrappers.Rules(rules_resource,
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
    #         self._rules = dict_wrappers.Rules(rules_resource)
    #     return self._application


    def update(self, **content):
        return self.__class__(self.resource.update(content),
                              self.client,
                              wallet=self.wallet)

    def pay(self, payees):
        content = dict(outputs=self.outputs_from_payees(payees))
        unsigned = self.resource.payments.create(content)

        transaction = Tx(data=unsigned.attributes)
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
        return list_wrappers.Transactions(transaction_resource, self.client)

    @property
    def addresses(self):
        address_resource = self.resource.addresses
        return list_wrappers.Addresses(address_resource, self.client)


class Transaction(Wrapper):
    def cancel(self):
        try:
            return self.resource.cancel()
        except Exception as e:
            print(e)
