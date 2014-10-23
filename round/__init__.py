# -*- coding: utf-8 -*-
# __init__.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import base64
import json
import patchboard

from pprint import pprint as pp
from datetime import date

# TODO: PSS when ruby can handle it.
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

from .client import Client


#default_url = u"http://api.gem.co/"
default_url = u"http://localhost:8998"

__patchboard_client = None

def client(url=default_url):
    global __patchboard_client

    if __patchboard_client is None:
        __patchboard_client = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(__patchboard_client.spawn())


def authenticate(**kwargs):
    url = kwargs.get(u'url', default_url)
    if u'developer' in kwargs:
        return _authenticate_developer(url, kwargs[u'developer'])
    elif u'application' in kwargs:
        return _authenticate_application(url, kwargs[u'application'])
    elif u'device' in kwargs:
        return _authenticate_device(url, kwargs[u'device'])
    elif u'otp' in kwargs:
        return _authenticate_otp(url, kwargs[u'otp'])
    else:
        raise ValueError(u"Supported authentication schemes are:\n{}".format(
            pp(client().schemes)))

def _authenticate_developer(api_url, developer):
    if 'email' in developer and 'privkey' in developer:
        _client = client(api_url)
        _client.context.authorize(u'Gem-Developer', **developer)
    else:
        raise ValueError(u'Must provide email and privkey')
    return _client

def _authenticate_application(api_url, application):
    if ('app_url' in application and
        'api_token' in application and
        'instance_id' in application):
        _client = client(api_url)
        _client.context.authorize(u'Gem-Application', **application)
    else:
        raise ValueError(u'Must provide app_url, api_token and instance_id')
    return _client

def _authenticate_device(api_url, device):
    if ('app_url' in device and
        'api_token' in device and
        'user_token' in device and
        'device_id' in device):
        _client = client(api_url)
        _client.context.authorize(u'Gem-Device', **otp)
    else:
        raise ValueError(u'Must provide app_url, api_token, user_token, and device_id')
    return _client

def _authenticate_otp(api_url, otp):
    if 'url' in otp and 'api_token' in otp and 'key' in otp and 'secret' in otp:
        _client = client(api_url)
        _client.context.authorize(u'Gem-OOB-OTP', **otp)
    else:
        raise ValueError(u'Must provide api_token, otp_key, and otp_secret')
    return _client


class Context(dict):

    def __init__(self):
        self.schemes = {
            u'Gem-Developer':
                {u'usage':
                     u"round.authenticate(developer={'email':email, 'privkey':pem_or_der_encoded_rsa_private_key} [, 'api_url':api_url]})"},
            u'Gem-Application':
                {u'usage':
                     u"round.authenticate(application={'app_url':app_url, 'api_token':token, 'instance_id':instance_id [, 'api_url':api_url]})"},
            u'Gem-Device':
                {u'usage':
                     u"round.authenticate(device={'app_url':app_url, 'api_token':token, 'user_token':token, 'device_id':device_id [, 'api_url':api_url]})"},
            u'Gem-OOB-OTP':
                {u'usage':
                     u"round.authenticate(otp={'api_token':token, 'key':otp_key, 'secret':otp_secret [, 'api_url':api_url]})"}
        }

    def authorizer(self, schemes, resource, action, request_args):
        if not schemes:
            return u'', u''
        for scheme in schemes:
            if scheme in self.schemes and u'credential' in self.schemes[scheme]:
                if scheme == u'Gem-Developer':
                    return scheme, u'{}, signature="{}"'.format(
                        self.schemes[scheme][u'credential'],
                        self.dev_signature(request_args[u'body']))
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
            return

        for field in [u'app_url', u'api_token',
                      u'user_token', u'device_id',
                      u'instance_id',
                      u'email', u'privkey']:
            if field in params:
                setattr(self, field, params[field])
                if field == u'privkey' or field == u'app_url':
                    del params[field]

        self.schemes[scheme][u'credential'] = Context.format_auth_params(params)


    def dev_signature(self, request_body):
        try:
            body = json.loads(request_body) if request_body else {}
            key = RSA.importKey(self.privkey)
            signer = PKCS1_v1_5.new(key)
            content = u'{}-{}'.format(json.dumps(body, separators=(',',':')), date.today().strftime('%Y/%m/%d'))
            digest = SHA256.new(content)
            return base64.urlsafe_b64encode(signer.sign(digest))
        except Exception as e:
            pp(e)
            raise Exception(u"You must provide a valid RSA private key.")

    @staticmethod
    def format_auth_params(params):
        parts = []
        for (key, value) in params.items():
            parts.append('{}="{}"'.format(key, value))
        return ", ".join(parts)
