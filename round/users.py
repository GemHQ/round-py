# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import *
from .errors import *
from .subscriptions import Subscriptions
from .devices import Devices
from .wallets import generate, Wallet


class Users(DictWrapper):
    """A collection of round.Users objects."""

    def create(self, email, device_name, passphrase=None,
               api_token=None, redirect_uri=None, **kwargs):
        """Create a new User object and add it to this Users collection.

        In addition to creating a user, this call will create a device for that
        user, whose device_token will be returned from this call. Store the
        device_token, as it's required to complete Gem-Device authentication
        after the user approves the device at the end of their signup flow.

        If you lose the device_token returned from users.create, you'll have to
        create a new device for the user to gain access to their account again.

        Also, after this call, be sure to redirect the user to the location in
        `mfa_uri` (second return value of this function) to complete their
        account.

        If you get a 409 Conflict error, then the user already exists in the Gem
        system and you'll want to do a
        `client.user(email).devices.create(device_name)`

        Args:
          email (str)
          device_name (str): Human-readable name for the device through which
            your Application will be authorized to access the new User's account.
          passphrase (str, optional): A passphrase with which to encrypt a user
            wallet. If not provided, a default_wallet parameter must be passed in
            kwargs.
          api_token (str, optional): Your app's API token. This is optional if
            and only if the Client which will be calling this function already
            has Gem-Application or Gem-Identify authentication.
          redirect_uri (str, optional): A URI to which to redirect the User after
            they confirm their Gem account.
          **kwargs

        Returns: device_token
        """

        if not passphrase and u'default_wallet' not in kwargs:
            raise ValueError("Usage: users.create(email, passphrase, device_name, api_token, redirect_uri)")
        elif passphrase:
            default_wallet = generate(passphrase, ['primary'])['primary']
        else:
            default_wallet = kwargs['default_wallet']

        default_wallet['name'] = 'default'
        default_wallet['primary_private_seed'] = default_wallet['encrypted_seed']
        default_wallet['primary_public_seed'] = default_wallet['public_seed']
        del default_wallet['encrypted_seed']
        del default_wallet['public_seed']
        del default_wallet['private_seed']

        # If not supplied, we assume the client already has an api_token param.
        if api_token:
            self.client.authenticate_identify(api_token)

        user_data = dict(email=email,
                         default_wallet=default_wallet,
                         device_name=device_name)

        if redirect_uri:
            user_data['redirect_uri'] = redirect_uri
        if 'first_name' in kwargs:
            user_data['first_name'] = kwargs['first_name']
        if 'last_name' in kwargs:
            user_data['last_name'] = kwargs['last_name']

        try:
            resource = self.resource.create(user_data)
        except ResponseError as e:
            if "conflict" in e.message:
                raise ConflictError("This user already exists. Use client.user(email).devices.create(name) to request authorization from the user.")
            raise e

        return resource.attributes['metadata']['device_token']

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
    def devices(self):
        if not hasattr(self, '_devices'):
            devices_resource = self.client.resources.devices_query(
                dict(email=self.email))
            self._devices = Devices(devices_resource, self.client)
        return self._devices

    @property
    def wallet(self):
        """Fetch and return this user's default (only) Wallet."""
        if not hasattr(self, '_wallet'):
            wallet_resource = self.default_wallet.get()
            self._wallet = Wallet(wallet_resource, self.client)
        return self._wallet

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions associated with this user."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions

    def send_mfa(self):
        """Send an SMS MFA token to the user."""
        return self.resource.send_mfa({})

    def verify_mfa(self, mfa_token):
        """Verify an SMS or TOTP MFA token for this user.

        Args:
          mfa_token (str): An alphanumeric code from either a User's TOTP
            application or sent to them via SMS.

        Returns:
          True if the mfa_token is valid, False otherwise.
        """
        response = self.resource.verify_mfa({'mfa_token': mfa_token})
        return (response['valid'] == True or response['valid'] == 'true')
