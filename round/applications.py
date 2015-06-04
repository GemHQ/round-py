# -*- coding: utf-8 -*-
# applications.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from pyotp import TOTP

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions
from .wallets import Wallets

import round.users


class Applications(DictWrapper):
    """A collection of Application objects"""

    def create(self, **kwargs):
        """Create a new Application.

        Args:
          **kwargs: Arbitrary keyword arguments, including:
          name (str): A name for the new Application.

        Returns:
           A round.Application object if successful.
        """
        resource = self.resource.create(kwargs)
        if 'admin_token' in kwargs:
            resource.context.authorize('Gem-Application',
                                       api_token=resource.api_token,
                                       admin_token=kwargs['admin_token'])
        app = self.wrap(resource)
        return self.add(app)

    def wrap(self, resource):
        return Application(resource, self.client)


class Application(Wrapper, Updatable):
    """Representation of a Gem integration.

    Attributes:
      api_token (str)
      totp (pyotp.TOTP): A TOTP MFA token generator (initialized with set_totp)
      users (round.Users): A collection of Users who have an active device
        authorization on this Application.
    """

    def set_totp(self, totp_secret):
        """Set the secret for generating MFA tokens to authorize

        Args:
          totp_secret (str): The secret token set on an Application in the Gem
            Developer Console.
        """
        self.totp = TOTP(totp_secret)
        return self

    def get_mfa(self):
        """Return the currently-valid MFA token for this application."""
        return self.totp.now()

    def reset(self, *args):
        """Resets any of the tokens for this Application.
        Note that you may have to reauthenticate afterwards.

        Usage:
          application.reset('api_token')
          application.reset('api_token', 'totp_secret')

        Args:
          *args (list of str): one or more of
            ['api_token', 'subscription_token', 'totp_secret']

        Returns:
          The Application.
        """
        self.resource = self.resource.reset(list(args))
        return self

    @property
    def users(self):
        if not hasattr(self, '_users'):
            users_resource = self.resource.users
            self._users = users.Users(users_resource, self.client)
        return self._users

    @property
    def wallets(self):
        """Fetch and return Wallets associated with this application."""
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = Wallets(wallets_resource,
                                    self.client, self)
        return self._wallets

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions associated with this account."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
