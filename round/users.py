# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions
from .devices import Device, Devices

import applications as apps
import wallets

class Users(DictWrapper):

    def create(self, email, **kwargs):
        backup_seed = None

        if ((u'passphrase' not in kwargs and
            u'default_wallet' not in kwargs) or
            u'device_name' not in kwargs or
            u'device_id' not in kwargs):
            raise ValueError("Usage: users.create(email, passphrase='new-wallet-passphrase', device_name='Device Name', device_id='device-uuid')")
        elif u'passphrase' in kwargs:
            backup_seed, wallet_data = wallets.generate(
                kwargs[u'passphrase'],
                network=self.client.network)

            del kwargs[u'passphrase']
            wallet_data[u'name'] = u'default'
            kwargs[u'default_wallet'] = wallet_data

        kwargs.update({u'email': email})
        device_name = kwargs.pop('device_name')
        device_id = kwargs.pop('device_id')
        api_token = kwargs.pop('api_token')

        resource = self.resource.create(kwargs)
        user = self.wrap(resource)

        # Creating a device launches the account confirmation email to the user,
        # and is required to give your application privileges on the user.
        device = user.devices.create(device_name, device_id, api_token=api_token)
        print device
        print device.attributes

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
            self._wallets = wallets.Wallets(wallets_resource, self.client)
        return self._wallets

    @property
    def devices(self):
        if not hasattr(self, '_devices'):
            devices_resource = self.resource.devices
            self._devices = Devices(devices_resource,
                                    self.client,
                                    populate=False)
        return self._devices

    @property
    def subscriptions(self):
        """
        Fetch and return Subscriptions associated with this user.
        """
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
