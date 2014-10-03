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

    def __init__(self):
        self.schemes = {
            u'Basic':
                {u'usage':
                     u"client.context.authorize('Basic', email, password)\n"},
            u'Gem-Application':
                {u'usage':
                     u"client.context.authorize('Gem-Application', url, api_token)\n"}
            }

    def authorizer(self, schemes, resource, action):
        for scheme in schemes:
            if u'credential' in self.schemes[scheme]:
                return scheme, self.schemes[scheme][u'credential']

        error_message = u""
        for scheme in schemes:
            error_message.append(self.schemes[scheme][u'usage']);

        raise Exception(
            u"You must first authorize your client\n{}".format(error_message))

    def authorize(self, scheme, **params):

        if u'Basic' == scheme:
            if u'email' in params and u'password' in params:
                self.email = params[u'email']
                self.password = params[u'password']
                self.schemes[scheme][u'credential'] = base64.b64encode(
                    u':'.join([self.email, self.password]))

        else:
            if u'url' in params:
                self.application_url = params[u'url']
            if u'api_token' in params:
                self.api_token = params[u'api_token']

            self.schemes[scheme][u'credential'] = format_auth_params(params)


    def format_auth_params(params):
        parts = []
        for (key, value) in params.items():
            parts.append('{}="{}"'.format(key, value))
        return ",".join(parts)
