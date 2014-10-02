# -*- coding: utf-8 -*-
# wrappers.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet
from coinop.bit.transaction import Transaction as Tx

import dict_wrappers
import list_wrappers

class Updatable(object):

    def update(self, **content):
        return self.__class__(self.resource.update(content))


class Wrapper(object):

    def __init__(self, resource):
        self.resource = resource

    def __getattr__(self, name):
        # TODO: may want to limit the delegation to specific attrs.
        return getattr(self.resource, name)


class Developers(object):

    def __init__(self, resource):
        self.resource = resource

    def create(self, **content):
        resource = self.resource.create(content)
        resource.context.set_developer(content[u'email'], content[u'password'])
        return self.wrap(resource)

    def wrap(self, resource):
        return Developer(resource=resource)


class Developer(Wrapper):

    def update(self, **content):
        resource = self.resource.update(content)

        email = resource.attributes.get(u'email', None)
        password = content.get(u'password', None)

        resource.context.set_developer(email=email, password=password)
        return Developer(resource)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            applications_resource = self.resource.applications
            self._applications = dict_wrappers.Applications(applications_resource)
        return self._applications


class User(Wrapper, Updatable):

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            applications_resource = self.resource.applications
            self._applications = dict_wrappers.Applications(applications_resource)
        return self._applications

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = dict_wrappers.Wallets(wallets_resource)
        return self._wallets


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
        if not hasattr(self, '_users'):
            users_resource = self.resource.users
            self._users = dict_wrappers.Users(users_resource)
        return self._users

    @property
    def rules(self):
        if not hasattr(self, '_rules'):
            rules_resource = self.resource.rules
            self._rules = dict_wrappers.Rules(rules_resource)
        return self._application


class Wallet(Wrapper, Updatable):

    def __init__(self, resource):
        super(Wallet, self).__init__(resource)

        self.multi_wallet = None

        ar = self.resource.accounts
        self.accounts = dict_wrappers.Accounts(resource=ar, wallet=self)

    @property
    def rules(self):
        if not hasattr(self, '_rules'):
            rules_resource = self.resource.rules
            self._rules = dict_wrappers.Rules(rules_resource)
        return self._application


    # def is_unlocked(self):
    #     return not self.is_locked()

    # def is_locked(self):
    #     return (self.multi_wallet is None)

    # def unlock(self, passphrase):
    #     wallet = self.resource
    #     primary_seed = PassphraseBox.decrypt(
    #         passphrase,
    #         wallet.primary_private_seed)

    #     self.multi_wallet = MultiWallet(
    #         private={u'primary': primary_seed},
    #         public={
    #             u'cosigner': wallet.cosigner_public_seed,
    #             u'backup': wallet.backup_public_seed})


    # Transfers are just payments.
    def transfer(self, value, source, destination):
        source_content = dict(url=source.url)
        dest_content = dict(url=destination.url)

        content = dict(
            value=value,
            source=source_content,
            destination=dest_content)
        unsigned = self.resource.payments.create(content)
        transaction = Tx(data=unsigned.attributes)
        signatures = self.signatures(transaction)

        transaction_hash = transaction.hex_hash()
        content = dict(inputs=signatures, transaction_hash=transaction_hash)
        signed = unsigned.sign(content)
        return signed

    def signatures(self, transaction):
        # TODO: output.metadata['type']['change']
        change_output = transaction.outputs[-1]
        if self.multi_wallet.is_valid_output(change_output):
            return self.multi_wallet.signatures(transaction)
        else:
            raise Exception('Problem with transaction: Invalid change address')


class Account(Wrapper, Updatable):

    def __init__(self, resource, wallet):
        super(Account, self).__init__(resource)
        self.wallet = wallet
        rules_resource = self.resource.rules

    @property
    def rules(self):
        if not hasattr(self, '_rules'):
            rules_resource = self.resource.rules
            self._rules = dict_wrappers.Rules(rules_resource)
        return self._application


    def update(self, **content):
        return self.__class__(self.resource.update(content), wallet=self.wallet)

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
        tr = self.resource.transactions(query)
        return list_wrappers.Transactions(resource=tr)

    @property
    def addresses(self):
        ar = self.resource.addresses
        return list_wrappers.Addresses(resource=ar)


class Transaction(Wrapper):
    pass
