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

__patchboard_client = None

def client(url=DEFAULT_URL, network=DEFAULT_NETWORK):
    global __patchboard_client

    if __patchboard_client is None:
        __patchboard_client = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(__patchboard_client.spawn(), network)


class Context(dict):

    def __init__(self):
        self.schemes = {
            u'Gem-Developer':
                {u'usage':
                     u"client.authenticate_developer(email=email, privkey=pem_or_der_encoded_rsa_private_key)",
                 u'params': [u'email', u'privkey']},
            u'Gem-Application':
                {u'usage':
                     u"client.authenticate_application(app_url=app_url, api_token=token, instance_id=instance_id)",
                 u'params': [u'app_url', u'api_token', u'instance_id']},
            u'Gem-Device':
                {u'usage':
                     u"client.authenticate_device(app_url=app_url, api_token=token, user_url=user_url, user_token=token, device_id=device_id)",
                 u'params': [u'app_url', u'api_token', u'user_url', u'user_token', u'device_id']},
            u'Gem-OOB-OTP':
                {u'usage':
                     u"client.authenticate_otp(api_token=token, key=otp_key, secret=otp_secret)",
                 u'params': [u'key', u'secret', u'api_token'],
                 u'credential':
                     u'data=none'}
        }

    def authorizer(self, schemes, resource, action, request_args):
        if not schemes:
            return u'', u''
        for scheme in schemes:
            if scheme in self.schemes and u'credential' in self.schemes[scheme]:
                if scheme == u'Gem-Developer':
                    sig, ts = self.dev_signature(request_args[u'body'])
                    return scheme, u'{}, signature="{}", timestamp="{}"'.format(
                        self.schemes[scheme][u'credential'], sig, ts)
                else:
                    return scheme, self.schemes[scheme][u'credential']

        error_message = u""
        for scheme in schemes:
            if scheme in self.schemes:
                error_message += self.schemes[scheme][u'usage'] + "\n"

        raise Exception(
            u"You must first authenticate your client\n{}".format(error_message))

    def authorize(self, scheme, **params):
        if scheme not in self.schemes:
            return False

        for field in self.schemes[scheme]['params']:
            if field in params:
                setattr(self, field, params[field])
                if field in [u'privkey', u'app_url', u'user_url']:
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
