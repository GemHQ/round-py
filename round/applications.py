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
from .users import Users


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
        token = str(self.totp.now())
        # PyOTP doesn't pre-pad tokens shorter than 6 characters
        # ROTP does, so we have to.
        while len(token) < 6:
            token = '0{}'.format(token)
        return token

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
    @cacheable
    def users(self):
        """Return the cached first page of users who have authorized this
        application.
        """
        return self.get_users()
    def get_users(self, page=0, fetch=True):
        """Return the specified page of users who have authorized this
        application.
        """
        return Users(self.resource.users, self.client, page=page, populate=fetch)

    @property
    @cacheable
    def wallets(self):
        """Return the cached first page of wallets owned by this application."""
        return self.get_wallets()
    def get_wallets(self, page=0, fetch=True):
        """Return the specified page of wallets owned by this application."""
        return Wallets(self.resource.wallets, self.client,
                       page=page, populate=fetch, application=self)

    @property
    @cacheable
    def subscriptions(self):
        """Return the cached first page of subscriptions associated with this
        application.
        """
        return self.get_subscriptions()
    def get_subscriptions(self, page=0, fetch=True):
        """Return the specified page of subscriptions associated with this
        application.
        """
        return Subscriptions(
            self.resource.subscriptions, self.client, page, populate=fetch)
