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


class Client(MFAable):
    """The Client object holds a connection to Gem and references to root-level
    objects.

    Attributes:
      context (round.Context)
      resources (patchboard.Resources)
      users (round.Users)
    """

    def __init__(self, pb_client, network=DEFAULT_NETWORK):
        self.pb_client = pb_client
        try:
            self.network = NETWORK_MAP[network]
            bitcoin.SelectParams(self.network)
        except:
            raise UnknownNetworkError(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.users = Users(self.resources.users, self)

    def authenticate_application(self, app_url, api_token, instance_token,
                                 override=False, fetch=True):
        """Set credentials for Application authentication.
        Important Note: Do not use Application auth on any end-user device.
        Application auth provides read-access to all Users who have
        authorized an Application. Use on a secure application server only.

        Args:
          app_url (str): URI for the Application in Gem's system.
            (api.gem.co/applications/:key)
          api_token (str): Token issued to your Application through the Gem
            Developer Console.
          instance_token (str): Token issued to run an instance of your App
            THIS IS A SECRET.
          override (boolean): Replace existing Application credentials.
          fetch (boolean): Return the authenticated Application.

        Returns:
          An Application object if `fetch` is True.
        """
        if (u'credential' in self.context.schemes[u'Gem-Application'] and
            not override):
            raise ValueError(u"This object already has Gem-Application authentication. To overwrite it call authenticate_application with override=True.")

        if (not app_url or not api_token or not instance_id or
            not self.context.authorize(u'Gem-Application',
                                       app_url=app_url,
                                       api_token=api_token,
                                       instance_token=instance_token)):
            raise ValueError(u"Usage: {}".format(
                self.context.schemes[u'Gem-Application'][u'usage']))

        return self.application if fetch else True

    def authenticate_device(self, api_token, device_id, email=None, user_url=None,
                            override=False, fetch=True):
        """Set credentials for Device authentication.

        Args:
          api_token (str): Token issued to your Application through the Gem
            Developer Console.
          device_id (str): Physical device identifier. You will receive this
            from a user.devices.create call or from users.create.
          email (str, optional): User's email address, required if user_url is
            not provided.
          user_url (str, optional): User's Gem url.
          override (boolean, optional): Replace existing Application credentials.
          fetch (boolean, optional): Return the authenticated User.

        Returns:
          An User object if `fetch` is True.
        """
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
        """Set credentials for Identify authentication.

        Args:
          api_token (str): Token issued to your Application through the Gem
            Developer Console.
          override (boolean): Replace existing Application credentials.
        """
        if (u'credential' in self.context.schemes[u'Gem-Identify'] and
            not override):
            raise ValueError(u"This object already has Gem-Idnetify authentication. To overwrite it call authenticate_identify with override=True.")

        if (not api_token or
            not self.context.authorize(u'Gem-Identify', api_token=api_token)):
            raise ValueError(u"Usage: {}".format(
                self.context.schemes[u'Gem-Identify'][u'usage']))

        return True

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
        wallet_resource = self.resources.wallet(url).get()
        return Wallet(wallet_resource, self)

    def account(self, url):
        account_resource = self.resources.account(url)
        return Account(account_resource, self)
