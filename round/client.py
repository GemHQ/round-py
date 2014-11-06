# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import bitcoin
import wrappers
import dict_wrappers

from pprint import pprint as pp

from .config import *

class Client(object):

    def __init__(self, pb_client, network=DEFAULT_NETWORK):
        self.pb_client = pb_client
        self.network = NETWORK_MAP[network]
        bitcoin.SelectParams(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.developers = wrappers.Developers(resource=self.resources.developers)
        self.users = dict_wrappers.Users(resource=self.resources.users)

    def authenticate(self, **kwargs):
        added = []
        if u'developer' in kwargs:
            added.append(authenticate_developer(**kwargs[u'developer']))
        if u'application' in kwargs:
            added.append(authenticate_application(**kwargs[u'application']))
        if u'device' in kwargs:
            added.append(authenticate_device(**kwargs[u'device']))
        if u'otp' in kwargs:
            added.append(authenticate_otp(**kwargs[u'otp']))
        if not added:
            raise ValueError(u"Supported authentication schemes are:\n{}".format(
                pp(client().schemes)))

    def authenticate_developer(self, email, privkey, override=False):
        if ('credential' in self.context.schemes[u'Gem-Developer'] and
            not override):
            raise ValueError(u"This object already has Gem-Developer authentication. To overwrite it call authenticate_developer with override=True.")

        if (not email or not privkey or
            not self.context.authorize(u'Gem-Developer', email=email, privkey=privkey)):
            raise ValueError(self.context.schemes[u'Gem-Developer']['usage'])

        return True

    def authenticate_application(self, app_url, api_token, instance_id):
        if ('credential' in self.context.schemes[u'Gem-Application'] and
            not override):
            raise ValueError(u"This object already has Gem-Application authentication. To overwrite it call authenticate_application with override=True.")

        if (not app_url or not api_token or not instance_id or
            not self.context.authorize(u'Gem-Application',
                                       app_url=app_url
                                       api_token=api_token,
                                       instance_id=instance_id)):
            raise ValueError(u'Must provide app_url, api_token and instance_id')

        return True

    def authenticate_device(app_url, api_token, user_url, user_token, device_id):
        if ('credential' in self.context.schemes[u'Gem-Device'] and
            not override):
            raise ValueError(u"This object already has Gem-Device authentication. To overwrite it call authenticate_device with override=True.")

        if (not app_url or not api_token or not user_url or
            not user_token or not device_id or
            not self.context.authorize(u'Gem-Device',
                                       app_url=app_url,
                                       api_token=api_token,
                                       user_url=user_url,
                                       user_token=user_token,
                                       device_id=device_id)):
            raise ValueError(u'Must provide app_url, api_token, user_url, user_token, and device_id')

        return True

    def authenticate_otp(api_token, key, secret):
        if ('credential' in self.context.schemes[u'Gem-OOB-OTP'] and
            not override):
            raise ValueError(u"This object already has Gem-OOB-OTP authentication. To overwrite it call authenticate_otp with override=True.")

        if (not api_token or not key or not secret or
            not self.context.authorize(u'Gem-OOB-OTP',
                                       api_token=api_token,
                                       key=key,
                                       secret=secret)):
            raise ValueError(u'Must provide api_token, key, and secret')

        return True

    @property
    def developer(self):
        if not hasattr(self, '_developer'):
            try:
                dev_resource = self.resources.developers.get()
                self._developer = wrappers.Developer(dev_resource)
            except Exception as e:
                raise Exception(
                    u"Authenticate this client with {} first".format(
                        self.context.schemes['Gem-Developer']['usage']))

        return self._developer

    @property
    def application(self):
        if not hasattr(self, '_application'):
            try:
                app_resource = self.resources.application(self.context.app_url).get()
                self._application = wrappers.Application(app_resource)
            except Exception as e:
                raise Exception(
                    u"Authenticate this client with {} first".format(
                        self.context.schemes['Gem-Application']['usage']))

        return self._application

    @property
    def user(self):
        if not hasattr(self, '_user'):
            try:
                user_resource = self.resources.user(self.context.user_url).get()
                self._user = wrappers.User(user_resource)
            except Exception as e:
                raise Exception(
                    u"Authenticate this client with {} first".format(
                        self.context.schemes['Gem-Device']['usage']))

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
