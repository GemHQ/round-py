# -*- coding: utf-8 -*-
# __init__.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import patchboard

# TODO: PSS when ruby can handle it.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from future.utils import iteritems
from copy import deepcopy

from .client import Client
from .config import *
from .errors import *

_patchboard = None

def client(url=None):
    global _patchboard

    if _patchboard is None:
        _patchboard = {}

    if not url:
        url = 'https://api.gem.co'

    if url not in _patchboard:
        _patchboard[url] = patchboard.discover(
            url, {'default_context': Context})
    return Client(_patchboard[url].spawn())


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
                 {u'params': {u'api_token': None,
                              u'admin_token': None},
                  u'usage': "client.authenticate_application(api_token, admin_token)"},
            u'Gem-Device':
                 {u'params': {u'api_token': None,
                              u'device_token': None},
                  u'usage': "client.authenticate_device(api_token, device_token, [email OR url])"},
            u'Gem-Identify':
                 {u'params': {u'api_token': None},
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
            if scheme in self.schemes and self.has_auth_params(scheme):
                cred = Context.format_auth_params(self.schemes[scheme][u'params'])
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
          True if parameters are set successfully (note that this doesn't mean
          the credentials are valid)
          False if the scheme specified is not supported
        """
        if scheme not in self.schemes:
            return False

        for field, value in iteritems(params):
            setattr(self, field, value)
            if field in self.schemes[scheme][u'params'].keys() and value:
                self.schemes[scheme][u'params'][field] = value

        return True

    def has_auth_params(self, scheme):
        """Check whether all information required for a given auth scheme have
        been supplied.

        Args:
          scheme (str): Name of the authentication scheme to check. One of
            Gem-Identify, Gem-Device, Gem-Application

        Returns:
          True if all required parameters for the specified scheme are present
          or False otherwise.
        """
        for k, v in iteritems(self.schemes[scheme][u'params']):
            if not v: return False
        return True

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
            if value:
                parts.append('{}="{}"'.format(key, value))
        return ", ".join(parts)
