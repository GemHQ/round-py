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
        return _authenticate_basic(url, kwargs['developer'])
        pass
    else:
        raise ValueError(u'Supply either user or application authentication')

def _authenticate_basic(api_url, developer):
    if 'email' in developer and 'password' in developer:
        _client = client(api_url)
        _client.context.set_developer(**developer)
        return _client
    else:
        raise ValueError(u'Must provide email and password')

def _authenticate_application(api_url, application):
    if 'url' in application and 'api_token' in application:
        _client = client(api_url)
        _client.context.set_application(**application)
        return _client
    else:
        raise ValueError(u'Must provide application url and token')

class Context(dict):

    def authorizer(self, schemes, resource, action):
        options = []
        if u"Basic" in schemes:
            if hasattr(self, u'basic'):
                return u"Basic", self.basic
            else:
                options.append(u"set_developer(email, password)")

        if u"Gem-Application" in schemes:
            if hasattr(self, u'api_token'):
                return u"Gem-Application", self.api_token
            else:
                options.append(u"set_application(url, api_token)")

        if schemes:
            message = u""
            for o in options:
                message += o + u"\n"
            raise Exception(
                u"You must authenticate with one of:\n{}".format(message))
        else:
            return None, None

    def set_developer(self, email=None, password=None):
        if email:
            self.email = email
        if password:
            self.password = password

        string = u':'.join([self.email, self.password])
        self.basic = base64.b64encode(string)

    def set_application(self, url, api_token):
        self.application_url = url
        self.api_token = api_token


