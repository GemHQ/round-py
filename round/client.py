# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import bitcoin

from .config import *
from wrappers import *
from errors import *
from developers import Developer, Developers
from users import User, Users
from applications import Application, Applications
from wallets import Wallet, Wallets
from accounts import Account, Accounts

from pprint import pprint as pp


class Client(object):

    def __init__(self, pb_client, network=DEFAULT_NETWORK):
        self.pb_client = pb_client
        try:
            self.network = NETWORK_MAP[network]
            bitcoin.SelectParams(self.network)
        except:
            raise UnknownNetworkError(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.developers = Developers(self.resources.developers, self)
        self.users = Users(self.resources.users, self)

    def authenticate(self, **kwargs):
        print u"client.authenticate() is DEPRECATED!"
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

    def with_mfa(self, mfa_token):
        self.context.mfa_token = mfa_token
        return self

    def authenticate_developer(self, key, email, session_token,
                               override=False, fetch=True):

        if not self.context.authorize(u'Gem-Developer-Session', key=key, session_token=session_token):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-Developer-Session'][u'usage']))

        return self.developer(email) if fetch else True

    def authenticate_user(self, key, email, session_token,
                          override=False, fetch=True):

        if not self.context.authorize(u'Gem-User-Session', key=key, session_token=session_token):
            raise ValueError("Usage: {}".format(
                self.context.schemes[u'Gem-User-Session'][u'usage']))

        return self.user(email) if fetch else True

    def authenticate_application(self, app_url, api_token, instance_id,
                                 override=False, fetch=True):
        if (u'credential' in self.context.schemes[u'Gem-Application'] and
            not override):
            raise ValueError(u"This object already has Gem-Application authentication. To overwrite it call authenticate_application with override=True.")

        if (not app_url or not api_token or not instance_id or
            not self.context.authorize(u'Gem-Application',
                                       app_url=app_url,
                                       api_token=api_token,
                                       instance_id=instance_id)):
            raise ValueError(u"Usage: {}".format(
                self.context.schemes[u'Gem-Application'][u'usage']))

        return self.application if fetch else True

    def authenticate_device(self, api_token, user_token, device_id, email=None,
                            user_url=None, override=False, fetch=True):
        if (u'credential' in self.context.schemes[u'Gem-Device'] and
            not override):
            raise ValueError(u"This object already has Gem-Device authentication. To overwrite it call authenticate_device with override=True.")

        if (not api_token or (not email and not user_url) or
            not user_token or not device_id or
            not self.context.authorize(u'Gem-Device',
                                       api_token=api_token,
                                       user_email=email,
                                       user_url=user_url,
                                       user_token=user_token,
                                       device_id=device_id)):
            raise ValueError(u"Usage: {}".format(
                self.context.schemes[u'Gem-Device'][u'usage']))
        if fetch:
            user = self.user(email) if email else self.user()
            return user.refresh()
        else:
            return True

    def authenticate_identify(self, api_token, override=True):
        if (u'credential' in self.context.schemes[u'Gem-Identify'] and
            not override):
            raise ValueError(u"This object already has Gem-Idnetify authentication. To overwrite it call authenticate_otp with override=True.")

        if (not api_token or
            not self.context.authorize(u'Gem-Identify', api_token=api_token)):
            raise ValueError(u"Usage: {}".format(
                self.context.schemes[u'Gem-Identify'][u'usage']))

        return True


    def begin_device_authorization(self, email, api_token, device_name,
                                   device_id):
        try:
            self.context.schemes[u'Gem-OOB-OTP'][u'credential'] = 'api_token="{}"'.format(api_token)
            reply = self.user(email).authorize_device({u'name': device_name,
                                                       u'device_id': device_id})
        except ResponseError as e:
            try:
                key = e.headers['WWW-Authenticate']['Gem-OOB-OTP'][u'key']
                return key
            except KeyError:
                if e.message == 'unauthorized':
                    raise OTPConflictError()
                else:
                    raise StandardError(e.message)
            except:
                raise e


    def complete_device_authorization(self, email, api_token, device_name,
                                      device_id, key, secret):
        try:
            self.authenticate_otp(api_token=api_token,
                                  key=key, secret=secret)

            r = self.user(email).authorize_device({u'name': device_name,
                                                   u'device_id': device_id})

        except ResponseError as e:
            try:
                new_key = e.headers['WWW-Authenticate']['Gem-OOB-OTP'][u'key']
                if new_key == key:
                    raise e
                else:
                    raise UnknownKeyError(new_key)
            except KeyError:
                raise e

        self.authenticate_device(api_token=api_token,
                                 user_url=r.url,
                                 user_token=r.user_token,
                                 device_id=device_id,
                                 override=True)

        return User(r, self)


    def developer(self, email=None):
        if not hasattr(self, u'_developer'):
            if email:
                dev_resource = self.resources.developer_query({u'email': email})
                self._developer = Developer(dev_resource.get(), self)

        return self._developer

    @property
    def application(self):
        if not hasattr(self, u'_application'):
            try:
                app_resource = self.resources.application(self.context.app_url).get()
                self._application = Application(app_resource, self)
            except AttributeError as e:
                raise AttributeError(
                    u"You must first authenticate this client with\n`{}`.".format(
                        self.context.schemes[u'Gem-Application'][u'usage']))

        return self._application

    def user(self, email=None):
        user_resource = False
        if not hasattr(self, '_user'):
            try:
                if email:
                    user_resource = self.resources.user_query({u'email': email})
                elif hasattr(self.context, u'user_url'):
                    user_resource = self.resources.user({u'url': self.context.user_url})
                else:
                    user_resource = self.resources.user_query({u'email': self.context.user_email})
            except AttributeError as e:
                raise AttributeError(
                    u"You must first authenticate this client with\n`{}`.".format(
                        self.context.schemes[u'Gem-Device'][u'usage']))

        elif email and (not hasattr(self._user, 'email') or
                        self._user.email != email):
            user_resource = self.resources.user_query({u'email': email})

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
