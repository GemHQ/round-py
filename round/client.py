# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import bitcoin
import wrappers
from .config import *


class Client(object):

    def __init__(self, pb_client, network=DEFAULT_NETWORK):
        self.pb_client = pb_client
        self.network = NETWORK_MAP[network]
        bitcoin.SelectParams(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.developers = wrappers.Developers(resource=self.resources.developers)

    @property
    def developer(self):
        if not hasattr(self, '_developer'):
            try:
                dev_resource = self.resources.developers.get()
                self._developer = wrappers.Developer(dev_resource)
            except:
                raise Exception(u"Instantiate a client with round.authenticate(developer={'email':email, 'privkey':rsa_private_key}) first")
        return self._developer

    @property
    def application(self):
        if not hasattr(self, '_application'):
            try:
                app_resource = self.resources.application(self.context.app_url).get()
                self._application = wrappers.Application(app_resource)
            except Exception as e:
                raise Exception(u"Instantiate a client using round.authenticate with device or application authentication first")
        return self._application

    @property
    def user(self):
        if not hasattr(self, '_user'):
            try:
                user_resource = self.resources.user(self.context.user_url).get()
                self._user = wrappers.User(user_resource)
            except:
                raise Exception(u"Instantiate a client using round.authenticate(device={app_url: app_url, api_token: token, user_url:user_url, user_token: token, device_id: device_id})")
        return self._user

    def wallet(self, url):
        # Not memoizing here, because a wallet is not a fundamental
        # part of a session, as a user or app would be.  Ditto account,
        # below.
        wallet_resource = self.resources.wallet(url).get()
        return wrappers.Wallet(wallet_resource)

    def account(self, url):
        account_resource = self.resources.account(url)
        return wrappers.Account(account_resource)
