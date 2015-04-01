# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions

import applications as apps
import wallets

class Users(DictWrapper):

    def create(self, email, passphrase, device_name, redirect_uri=None, api_token=None, **kwargs):
        if not passphrase and u'default_wallet' not in kwargs:
            raise ValueError("Usage: users.create(email, passphrase='new-wallet-passphrase', device_name, device_id, api_token)")
        elif passphrase:
            default_wallet = wallets.generate(passphrase,
                                              network=self.client.network)
            default_wallet[u'name'] = u'default'

        # If not supplied, we assume the client already has an api_token param.
        if api_token:
            self.client.authenticate_identify(api_token)

        user_data = dict(email=email,
                         default_wallet=default_wallet,
                         redirect_uri=redirect_uri,
                         device_name=device_name)
        if u'first_name' in kwargs:
            user_data[u'first_name'] = kwargs[u'first_name']
        if u'last_name' in kwargs:
            user_data[u'last_name'] = kwargs[u'last_name']
        resource = self.resource.create(user_data)
        user = self.wrap(resource)
        return self.add(user)

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
        """Fetch and return Subscriptions associated with this user."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
