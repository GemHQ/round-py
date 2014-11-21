# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import bitcoin

from .config import *
from wrappers import *
from developers import Developer, Developers
from users import User, Users
from applications import Application, Applications
from wallets import Wallet, Wallets
from accounts import Account, Accounts

from pprint import pprint as pp


class Client(object):

    def __init__(self, pb_client, network=DEFAULT_NETWORK):
        self.pb_client = pb_client
        self.network = NETWORK_MAP[network]
        bitcoin.SelectParams(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.developers = Developers(self.resources.developers, self)
        self.users = Users(self.resources.users, self)

    def authenticate(self, **kwargs):
        added = []
        if u'developer' in kwargs:
            added.append(self.authenticate_developer(**kwargs[u'developer']))
        if u'application' in kwargs:
            added.append(self.authenticate_application(**kwargs[u'application']))
        if u'device' in kwargs:
            added.append(self.authenticate_device(**kwargs[u'device']))
        if u'otp' in kwargs:
            added.append(self.authenticate_otp(**kwargs[u'otp']))
        if not added:
            raise ValueError(u"Supported authentication schemes are:\n{}".format(
                pp(client().schemes)))
        return added

    def authenticate_developer(self, email, privkey, timestamp,
                               override=False, fetch=True):
        if ('credential' in self.context.schemes[u'Gem-Developer'] and
            not override):
            raise ValueError(u"This object already has Gem-Developer authentication. To overwrite it call authenticate_developer with override=True.")

        if (not email or not privkey or not timestamp or
            not self.context.authorize(u'Gem-Developer', email=email, privkey=privkey, timestamp=timestamp)):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-Developer']['usage']))

        return self.developer if fetch else True

    def authenticate_application(self, app_url, api_token, instance_id,
                                 override=False, fetch=True):
        if ('credential' in self.context.schemes[u'Gem-Application'] and
            not override):
            raise ValueError(u"This object already has Gem-Application authentication. To overwrite it call authenticate_application with override=True.")

        if (not app_url or not api_token or not instance_id or
            not self.context.authorize(u'Gem-Application',
                                       app_url=app_url,
                                       api_token=api_token,
                                       instance_id=instance_id)):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-Application']['usage']))

        return self.application if fetch else True

    def authenticate_device(self, api_token, user_token, device_id, email=None,
                            user_url=None, app_url=None, override=False,
                            fetch=True):
        if ('credential' in self.context.schemes[u'Gem-Device'] and
            not override):
            raise ValueError(u"This object already has Gem-Device authentication. To overwrite it call authenticate_device with override=True.")

        if (not api_token or (not email and not user_url) or
            not user_token or not device_id or
            not self.context.authorize(u'Gem-Device',
                                       app_url=app_url,
                                       api_token=api_token,
                                       user_email=email,
                                       user_url=user_url,
                                       user_token=user_token,
                                       device_id=device_id)):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-Device']['usage']))

        return self.user if fetch else True

    def authenticate_otp(self, api_token, key, secret, override=True):
        if ('credential' in self.context.schemes[u'Gem-OOB-OTP'] and
            not override):
            raise ValueError(u"This object already has Gem-OOB-OTP authentication. To overwrite it call authenticate_otp with override=True.")

        if (not api_token or not key or not secret or
            not self.context.authorize(u'Gem-OOB-OTP',
                                       api_token=api_token,
                                       key=key,
                                       secret=secret)):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-OOB-OTP']['usage']))

        return True

    @property
    def developer(self):
        if not hasattr(self, '_developer'):
            try:
                dev_resource = self.resources.developers.get()
                self._developer = Developer(dev_resource, self)
            except AttributeError as e:
                # TODO: Add AuthenticationError
                raise AttributeError(
                    u"You must first authenticate this client with\n`{}`.".format(
                        self.context.schemes['Gem-Developer']['usage']))

        return self._developer

    @property
    def application(self):
        if not hasattr(self, '_application'):
            try:
                app_resource = self.resources.application(self.context.app_url).get()
                self._application = Application(app_resource, self)
            except AttributeError as e:
                raise AttributeError(
                    u"You must first authenticate this client with\n`{}` or\n`{}`.".format(
                        self.context.schemes['Gem-Application']['usage'],
                        self.context.schemes['Gem-Device']['usage']))

        return self._application

    @property
    def user(self, email=None):
        user_resource = False
        if not hasattr(self, '_user'):
            try:
                if email:
                    user_resource = self.resources.user(email)
                elif hasattr(self.context, u'user_url'):
                    user_resource = self.resources.user(self.context.user_url)
                else:
                    user_resource = self.resources.user_query(self.context.user_email)
            except AttributeError as e:
                raise AttributeError(
                    u"You must first authenticate this client with\n`{}`.".format(
                        self.context.schemes['Gem-Device']['usage']))

        elif email and self._user.email != email:
            user_resource = self.resources.user(email)

        if user_resource:
            self._user = User(user_resource, self)
            # Fetch the user if we can. If not, we're probably just getting a
            # resource so we can do authorize_device.
            try:
                self._user.refresh()
            except:
                pass

        return self._user

    def wallet(self, url):
        # Not memoizing here, because a wallet is not a fundamental
        # part of a session, as a user or app would be.  Ditto account,
        # below.
        wallet_resource = self.resources.wallet(url).get()
        return Wallet(wallet_resource, self)

    def account(self, url):
        account_resource = self.resources.account(url)
        return Account(account_resource, self)
