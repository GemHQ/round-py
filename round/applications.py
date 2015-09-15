# -*- coding: utf-8 -*-
# applications.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from pyotp import TOTP

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions
from .wallets import Wallets
from .users import Users
from .netki import NetkiDomains

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
        """Returned the cached Users associated with this application."""
        return self.get_users()

    def get_users(self, fetch=True):
        """Return this Applications's users object, populating it if fetch
        is True."""
        return Users(self.resource.users, self.client, populate=fetch)

    @property
    @cacheable
    def wallets(self):
        """Returned the cached Wallets associated with this application."""
        return self.get_wallets()

    def get_wallets(self, fetch=False):
        """Return this Applications's wallets object, populating it if fetch
        is True."""
        return Wallets(
            self.resource.wallets, self.client, populate=fetch, application=self)

    @property
    @cacheable
    def subscriptions(self):
        """Return the cached Subscriptions object for this Application."""
        return self.get_subscriptions()

    def get_subscriptions(self, fetch=True):
        """Return this Application's subscriptions object, populating it if
        fetch is True."""
        return Subscriptions(
            self.resource.subscriptions, self.client, populate=fetch)

    def wallet(self, key):
        return self.client.wallet(key, application=self)

    @property
    @cacheable
    def netki_domains(self):
        """Fetch and return an updated list of NetkiDomains inside this
        Application."""
        return self.get_netki_domains()

    def get_netki_domains(self, fetch=False):
        """Return the Applications NetkiDomains object, populating it if fetch
        is True."""
        return NetkiDomains(
            self.resource.netki_domains, self.client, populate=fetch)
