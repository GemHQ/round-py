# -*- coding: utf-8 -*-
# dict_wrappers.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import abc
import collections

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

import wrappers


class DictWrapper(collections.Mapping):

    def __init__(self, resource):
        self.resource = resource
        self.data = {}
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def populate(self):
        # TODO: checking for 'list' is probably unnecessary
        # after the refactor into dict wrapper
        if hasattr(self.resource, u'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.add(wrapper)

    def add(self, wrapper):
        key = self.key_for(wrapper)
        self.data[key] = wrapper

    def refresh(self):
        self.data = {}
        self.populate()
        return(self)

    def key_for(self, wrapper):
        return wrapper.name

    @abc.abstractmethod
    def wrap(self, resource):
        pass

class Rules(collections.Mapping):

    def __init__(self, resource):
        self.resource = resource
        self.refresh()

    def __getitem__(self, name):
        return self.definitions.__getitem__(name)

    def __iter__(self):
        return self.definitions.__iter__()

    def __len__(self):
        return self.definitions.__len__()

    def refresh(self):
        self.cache = self.resource.get()
        self.definitions = {}
        for key, value in self.cache.definitions.iteritems():
            self.definitions[key] = self.wrap(value)
        return self

    def wrap(self, resource):
        return wrappers.Rule(resource=resource)

    def add(self, name):
        return self.wrap(self.resource.add(dict(name=name)))


class Applications(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        # FIXME:  probably need to imitate what the Ruby client is doing here.
        resource.context.set_application(url=resource.url, token=resource.api_token)
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Application(resource=resource)


class Users(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        user = self.wrap(resource)
        self.add(user)
        return user

    def wrap(self, resource):
        return wrappers.User(resource=resource)


class Wallets(DictWrapper):

    # The passphrase parameter should stay out of the content dict
    # so that there is no chance the client's passphrase will get passed
    # to our server.
    def create(self, passphrase, **content):
        multi_wallet = MultiWallet.generate([u'primary', u'backup'])

        primary_seed = multi_wallet.private_seed(u'primary')
        backup_seed = multi_wallet.private_seed(u'backup')

        primary_public_seed = multi_wallet.public_seed(u'primary')
        backup_public_seed = multi_wallet.public_seed(u'backup')

        encrypted_seed = PassphraseBox.encrypt(passphrase, primary_seed)

        content[u'network'] = u'bitcoin_testnet'
        content[u'backup_public_seed'] = backup_public_seed
        content[u'primary_public_seed'] = primary_public_seed
        content[u'primary_private_seed'] = encrypted_seed

        resource = self.resource.create(content)
        wallet = self.wrap(resource)
        self.add(wallet)
        return backup_seed, wallet

    def wrap(self, resource):
        return wrappers.Wallet(resource=resource)


class Accounts(DictWrapper):

    def __init__(self, resource, wallet):
        self.wallet = wallet
        super(Accounts, self).__init__(resource)

    def create(self, **content):
        resource = self.resource.create(content)
        acc = self.wrap(resource)
        self.add(acc)
        return acc

    def wrap(self, resource):
        return wrappers.Account(resource=resource, wallet=self.wallet)
