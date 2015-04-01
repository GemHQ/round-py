# -*- coding: utf-8 -*-
# __init__.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import base64
import json
import patchboard

from pprint import pprint as pp
from time import time

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
        _patchboard[url] = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(_patchboard[url].spawn(), network)


class Context(dict):

    def __init__(self):
        self.schemes = {
            u'Gem-Developer-Session':
                {u'usage':
                     u"DEPRECATE",
                 u'params': [u'key', u'session_token']},
            u'Gem-User-Session':
                {u'usage':
                     u"DEPRECATE",
                 u'params': [u'key', u'session_token']},
            u'Gem-Application':
                {u'usage':
                     u"client.authenticate_application(app_url=app_url, api_token=token, instance_id=instance_id [, override=False, fetch=True])",
                 u'params': [u'app_url', u'api_token', u'instance_id']},
            u'Gem-Device':
                {u'usage':
                     u"client.authenticate_device(api_token=token, user_token=token, device_id=device_id [, email=user_email, user_url=user_url, override=False, fetch=True])",
                 u'params': [u'api_token', u'user_email', u'user_url', u'user_token', u'device_id']},
            u'Gem-Identify':
                {u'usage':
                     u"client.authenticate_identify(api_token=token [, override=False])",
                 u'params': [u'api_token']},
            u'Gem-MFA':
                {u'usage':
                     u"client.authenticate_mfa(auth_token=token [, mfa_token=token])",
                 u'params': [u'auth_token']},
            u'Gem-Password':
                {u'usage':
                     u"client.authenticate_password(auth_token=token [, mfa_token=token])",
                 u'params': [u'password_hash']}
        }

    def authorizer(self, schemes, resource, action, request_args):
        if not schemes:
            return u'', u''
        for scheme in schemes:
            if scheme in self.schemes and u'credential' in self.schemes[scheme]:
                creds = self.schemes[scheme][u'credential']
                if hasattr(self, 'mfa_token'):
                    creds = '{}, mfa_token="{}"'.format(creds, self.mfa_token)
                return scheme, creds


        raise AuthenticationError(self, schemes)

    def authorize(self, scheme, **params):
        if scheme not in self.schemes:
            return False

        for field in self.schemes[scheme]['params']:
            if field in params and params[field]:
                setattr(self, field, params[field])
            if field in [u'privkey', u'app_url', u'user_url', u'user_email']:
                del params[field]

        self.schemes[scheme][u'credential'] = Context.format_auth_params(params)
        return self.schemes[scheme][u'credential']


    def dev_signature(self, request_body):
        try:
            body = json.loads(request_body) if request_body else {}
            key = RSA.importKey(self.privkey)
            signer = PKCS1_v1_5.new(key)
            ts = int(time())
            content = u'{}-{}'.format(json.dumps(body, separators=(',',':')), ts)
            digest = SHA256.new(content)
            return base64.urlsafe_b64encode(signer.sign(digest)), ts
        except Exception as e:
            pp(e)
            raise Exception(u"You must provide a valid RSA private key.")

    @staticmethod
    def format_auth_params(params):
        parts = []
        for (key, value) in params.items():
            parts.append('{}="{}"'.format(key, value))
        return ", ".join(parts)
