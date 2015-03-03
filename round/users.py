# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
import applications as apps
import wallets

class Users(DictWrapper):

    def create(self, email, **kwargs):
        backup_seed = None

        if u'passphrase' not in kwargs and u'default_wallet' not in kwargs:
            raise ValueError("Usage: users.create(email, passphrase='new-wallet-passphrase')")
        elif u'passphrase' in kwargs:
            backup_seed, wallet_data = wallets.generate(
                kwargs[u'passphrase'],
                network=self.client.network)

            del kwargs[u'passphrase']
            wallet_data[u'name'] = u'default'
            kwargs[u'default_wallet'] = wallet_data

        kwargs.update({u'email': email})

        resource = self.resource.create(kwargs)
        user = self.wrap(resource)
        self.add(user)
        return backup_seed, user

    def wrap(self, resource):
        return User(resource, self.client)

    def key_for(self, wrapper):
        return wrapper.email


class User(Wrapper, Updatable):

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource, self.client)

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = wallets.Wallets(wallets_resource,
                                            self.client)
        return self._wallets

    @property
    def subscriptions(self):
        """
        Fetch and return Subscriptions associated with this user.
        """
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = subscriptions.Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
