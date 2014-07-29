# __init__.py
#
# Copyright 2014 BitVault.


import base64

import patchboard

from .client import Client


default_url = u"http://bitvault.pandastrike.com/"


__patchboard_client = None

def client(url=default_url):
    global __patchboard_client

    if __patchboard_client is None:
        __patchboard_client = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(__patchboard_client.spawn())


def authenticate(**options):
    url = options.get('url', default_url)
    if 'application' in options:
        return _authenticate_application(url, **options['application'])
    elif 'user' in options:
        return _authenticate_user(url, **options['user'])
        pass
    else:
        raise ValueError(u'Supply either user or application authentication')

def _authenticate_user(api_url, **user):
    if 'email' in user and 'password' in user:
        _client = client(api_url)
        _client.context.set_user(**user)
        return _client
    else:
        raise ValueError(u'Must provide email and password')

def _authenticate_application(api_url, **application):
    if 'url' in application and 'token' in application:
        _client = client(api_url)
        _client.context.set_application(**application)
        return _client
    else:
        raise ValueError(u'Must provide application url and token')

class Context(dict):

    def authorizer(self, scheme, resource, action):
        if scheme == u"Basic":
            if hasattr(self, u'basic'):
                return self.basic
            else:
                raise Exception(u"Must call set_user(email, password) first")

        elif scheme == u"BitVault-Token":
            if hasattr(self, u'api_token'):
                return self.api_token
            else:
                raise Exception(u"Must call set_application(url, token) first")


    def set_user(self, email, password):
        self.email = email
        self.password = password
        string = u':'.join([email, password])
        self.basic = base64.b64encode(string)

    def set_application(self, url, token):
        self.application_url = url
        self.api_token = token


