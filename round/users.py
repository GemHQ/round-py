# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions

import applications as apps
import wallets

class Users(DictWrapper):
    """A collection of round.Users objects."""

    def create(self, email, device_name, passphrase=None,
               redirect_uri=None, api_token=None, **kwargs):
        """Create a new User object and add it to this Users collection.

        In addition to creating a user, this call will create a device for that
        user, whose device_id will be returned from this call. Store the
        device_id, as it's required to complete Gem-Device authentication after
        the user approves the device at the end of their signup flow.

        After this call, be sure to redirect the user to the user.mfa_uri
        location to complete their account. If you get a 409 Conflict error, then
        the user already exists in the Gem system and you'll want to do a
        `client.user(email).devices.create(device_name)`

        Args:
          email (str)
          device_name (str): Human-readable name for the device through which
            your Application will be authorized to access the new User's account.
          passphrase (str, optional): A passphrase with which to encrypt a user
            wallet. If not provided, a default_wallet parameter must be passed in
            kwargs.
          redirect_uri (str, optional): A URI to which to redirect the User after
            they confirm their Gem account.
          api_token (str, optional): Your app's API token. This is optional if
            and only if the Client which will be calling this function already
            has Gem-Application or Gem-Identify authentication.
          **kwargs

        Returns: A tuple of (device_id, round.User)
        """

        if not passphrase and u'default_wallet' not in kwargs:
            raise ValueError("Usage: users.create(email, passphrase, device_name, redirect_uri, api_token)")
        elif passphrase:
            default_wallet = wallets.generate(
                passphrase, network=self.client.network)[u'primary']
        else:
            default_wallet = kwargs[u'default_wallet']

        default_wallet[u'name'] = 'default'
        default_wallet[u'primary_private_seed'] = default_wallet[u'encrypted_seed']
        default_wallet[u'primary_public_seed'] = default_wallet[u'public_seed']
        del default_wallet[u'encrypted_seed']
        del default_wallet[u'public_seed']
        del default_wallet[u'private_seed']

        # If not supplied, we assume the client already has an api_token param.
        if api_token:
            self.client.authenticate_identify(api_token)

        user_data = dict(email=email,
                         default_wallet=default_wallet,
                         device_name=device_name)

        if redirect_uri:
            user_data[u'redirect_uri'] = redirect_uri
        if u'first_name' in kwargs:
            user_data[u'first_name'] = kwargs[u'first_name']
        if u'last_name' in kwargs:
            user_data[u'last_name'] = kwargs[u'last_name']

        resource = self.resource.create(user_data)
        return resource.attributes[u'device_id'], self.wrap(resource)

    def wrap(self, resource):
        return User(resource, self.client)

    def key_for(self, wrapper):
        return wrapper.email


class User(Wrapper, Updatable):
    """A User represents an single *human* end-user.
    A User will have sole access to their backup key, and will need to
    communicate directly with Gem to provide MFA credentials for protected
    actions (updating their User object, publishing transactions, approving
    devices, etc).

    For a custodial model where a Wallet is intended to hold assets of multiple
    individuals or an organization, read the Gem docs regarding Application
    wallets.

    Attributes:
      first_name (str)
      last_name (str)
      email (str)
      phone_number (str)
      default_wallet (round.Wallet)
      wallets (round.Wallets)
      devices (list)
    """

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource, self.client)

    @property
    def wallets(self):
        """Fetch and return Wallets associated with this user."""
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = wallets.Wallets(wallets_resource,
                                            self.client)
        return self._wallets

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions associated with this user."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
