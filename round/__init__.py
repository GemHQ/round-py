# -*- coding: utf-8 -*-
# __init__.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import patchboard

# TODO: PSS when ruby can handle it.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from .client import Client
from .config import *
from .errors import *

_patchboard = None

def client(url=DEFAULT_URL, network=DEFAULT_NETWORK):
    global _patchboard

    if _patchboard is None:
        _patchboard = {}

    if url not in _patchboard:
        _patchboard[url] = patchboard.discover(
            url, {u'default_context': Context})
    return Client(_patchboard[url].spawn(), network)


class Context(dict):
    """Context holds parameters for authenticating to Gem under various schemes.
    This class allows for multiple concurrent authentication levels. It can only
    hold one instance of any parameter, so new Contexts should be created to
    store multiple instances of the same scheme.

    __init__ takes no arguments.

    Attributes:
      schemes (dict of dict): A collection whose keys are authentication schemes
        supported by Gem and whose values are dicts containing parameters and
        credentials for that scheme.
    """

    def __init__(self):
        self.schemes = {
            u'Gem-Application':
                 {u'params': [u'app_url', u'api_token', u'instance_token'],
                  u'usage': "client.authenticate_application(app_url, api_token, instance_token)"},
            u'Gem-Device':
                 {u'params': [u'api_token', u'device_id', u'user_email',
                              u'user_url'],
                  u'usage': "client.authenticate_device(api_token, device_id, email)"},
            u'Gem-Identify':
                 {u'params': [u'api_token'],
                  u'usage': "client.authenticate_identify(api_token)"}}

    def authorizer(self, schemes, resource, action, request_args):
        """Construct the Authorization header for a request.

        Args:
          schemes (list of str): Authentication schemes supported for the
            requested action.
          resource (str): Object upon which an action is being performed.
          action (str): Action being performed.
          request_args (list of str): Arguments passed to the action call.

        Returns:
          (str, str) A tuple of the auth scheme satisfied, and the credential
            for the Authorization header or empty strings if none could be
            satisfied.
        """
        if not schemes:
            return u'', u''
        for scheme in schemes:
            if scheme in self.schemes and u'credential' in self.schemes[scheme]:
                cred = self.schemes[scheme][u'credential']
                if hasattr(self, 'mfa_token'):
                    cred = '{}, mfa_token="{}"'.format(cred, self.mfa_token)
                return scheme, cred

        raise AuthenticationError(self, schemes)

    def authorize(self, scheme, **params):
        """Store credentials required to satisfy a given auth scheme.

        Args:
          scheme (str): The name of the Authentication scheme.
          **params: parameters for the specified scheme.

        Returns:
          The Authorization header string generated for the scheme.
        """
        if scheme not in self.schemes:
            return False

        # TODO: Do we store params on the scheme when they were provided or
        # (as is the current case) globally, accessible to all schmes?
        for field in self.schemes[scheme]['params']:
            if field in params and params[field]:
                setattr(self, field, params[field])
            if field in [u'app_url', u'user_url', u'user_email']:
                del params[field]

        self.schemes[scheme][u'credential'] = Context.format_auth_params(params)
        return self.schemes[scheme][u'credential']

    @staticmethod
    def format_auth_params(params):
        """Generate the format expected by HTTP Headers from parameters.

        Args:
          params (dict): {key: value} to convert to key=value

        Returns:
          A formatted header string.
        """
        parts = []
        for (key, value) in params.items():
            parts.append('{}="{}"'.format(key, value))
        return ", ".join(parts)
