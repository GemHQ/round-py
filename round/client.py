# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

import bitcoin

from .config import *

from .wrappers import *
from .errors import *
from .developers import Developer, Developers
from .users import User, Users
from .applications import Application, Applications
from .wallets import Wallet, Wallets
from .accounts import Account, Accounts

class Client(MFAable):
    """The Client object holds a connection to Gem and references to root-level
    objects.

    Attributes:
      context (round.Context)
      resources (patchboard.Resources)
      users (round.Users)
    """

    def __init__(self, pb_client):
        self.pb_client = pb_client
        #try:
            #self.network = NETWORK_MAP[network]
            #bitcoin.SelectParams(self.network)
        #except:
            #raise UnknownNetworkError(network)
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.users = Users(self.resources.users, self)

    def authenticate_application(self, api_token, admin_token,
                                 override=False, fetch=True):
        """Set credentials for Application authentication.
        Important Note: Do not use Application auth on any end-user device.
        Application auth provides read-access to all Users who have
        authorized an Application. Use on a secure application server only.

        Args:
          api_token (str): Token issued to your Application through the Gem
            Developer Console.
          admin_token (str): Token issued to run an instance of your App
            THIS IS A SECRET. TREAT IT LIKE A SECRET.
          override (boolean): Replace existing Application credentials.
          fetch (boolean): Return the authenticated Application.

        Returns:
          An Application object if `fetch` is True.
        """
        if (self.context.has_auth_params('Gem-Application') and not override):
            raise OverrideError('Gem-Application')

        if (not api_token or not admin_token or
            not self.context.authorize('Gem-Application',
                                       api_token=api_token,
                                       admin_token=admin_token)):
            raise AuthUsageError(self.context, 'Gem-Application')

        return self.application if fetch else True

    def authenticate_device(self, api_token, device_token, email=None,
                            user_url=None, override=False, fetch=True):
        """Set credentials for Device authentication.

        Args:
          api_token (str): Token issued to your Application through the Gem
            Developer Console.
          device_token (str): Physical device identifier. You will receive this
            from a user.devices.create call or from users.create.
          email (str, optional): User's email address, required if user_url is
            not provided.
          user_url (str, optional): User's Gem url.
          override (boolean, optional): Replace existing Application credentials.
          fetch (boolean, optional): Return the authenticated User.

        Returns:
          An User object if `fetch` is True.
        """
        if (self.context.has_auth_params('Gem-Device') and not override):
            raise OverrideError('Gem-Device')

        if (not api_token or
            not device_token or
            (not email and not user_url) or
            not self.context.authorize('Gem-Device',
                                       api_token=api_token,
                                       user_email=email,
                                       user_url=user_url,
                                       device_token=device_token)):
            raise AuthUsageError(self.context, 'Gem-Device')

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
        if (self.context.has_auth_params('Gem-Identify') and not override):
            raise OverrideError('Gem-Identify')

        if (not api_token or
            not self.context.authorize('Gem-Identify', api_token=api_token)):
            raise AuthUsageError(self.context, 'Gem-Identify')

        return True

    @property
    def application(self):
        if not hasattr(self, '_application'):
            try:
                app_resource = self.resources.app.get()
                self._application = Application(app_resource, self)
            except AttributeError as e:
                raise AuthenticationError(self.context, 'Gem-Identify')

        return self._application

    def user(self, email=None):
        user_resource = False
        if not hasattr(self, '_user'):
            try:
                if email:
                    user_resource = self.resources.user_query({'email': email})
                elif hasattr(self.context, 'user_url'):
                    user_resource = self.resources.user({'url': self.context.user_url})
                else:
                    user_resource = self.resources.user_query({'email': self.context.user_email})
            except AttributeError as e:
                raise AuthenticationError(self.context, 'Gem-Device')

        elif email:
            user_resource = self.resources.user_query({'email': email})

        if user_resource:
            self._user = User(user_resource, self)
            setattr(user_resource, 'email', email)
            # Fetch the user if we can. If not, we're probably just getting a
            # resource so we can do authorize_device.
            try:
                self._user.refresh()
            except:
                pass

        return self._user
