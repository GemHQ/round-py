# __init__.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import base64

import patchboard

from .client import Client


default_url = u"http://api.gem.co/"

__patchboard_client = None

def client(url=default_url):
    global __patchboard_client

    if __patchboard_client is None:
        __patchboard_client = patchboard.discover(url,
                                                  {u'default_context': Context})
    return Client(__patchboard_client.spawn())


def authenticate(**kwargs):
    url = kwargs.get('url', default_url)
    if 'application' in kwargs:
        return _authenticate_application(url, kwargs['application'])
    elif 'developer' in kwargs:
        return _authenticate_developer(url, kwargs['user'])
        pass
    else:
        raise ValueError(u'Supply either user or application authentication')

def _authenticate_basic(api_url, developer):
    if 'email' in developer and 'password' in developer:
        _client = client(api_url)
        _client.context.set_developer(**user)
        return _client
    else:
        raise ValueError(u'Must provide email and password')

def _authenticate_application(api_url, application):
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
                raise Exception(u"Must call set_developer(email, password) first")

        elif scheme == u"Gem-Token":
            if hasattr(self, u'api_token'):
                return self.api_token
            else:
                raise Exception(u"Must call set_application(url, token) first")


    def set_developer(self, email=None, password=None):
        if email:
            self.email = email
        if password:
            self.password = password

        string = u':'.join([self.email, self.password])
        self.basic = base64.b64encode(string)

    def set_application(self, url, token):
        self.application_url = url
        self.api_token = token


