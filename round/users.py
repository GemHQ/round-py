# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from wrappers import *


class Users(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        user = self.wrap(resource)
        self.add(user)
        return user

    def wrap(self, resource):
        return wrappers.User(resource, self.client)

    def key_for(self, wrapper):
        return wrapper.email


class User(Wrapper, Updatable):

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource, self.client)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            apps_resource = self.resource.applications
            self._applications = Applications(apps_resource,
                                              self.client)
        return self._applications

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = Wallets(wallets_resource,
                                    self.client)
        return self._wallets

    def authorize_device(self, **content):
        try:
            reply = self.resource.authorize_device(content)
            # Doesn't require the app_url, since that is only for the
            # client.application convenience method.
            self.resource.context.authorize(scheme='Gem-Device',
                                            api_token=self.context.api_token,
                                            user_url=self.url,
                                            user_token=self.user_token,
                                            device_id=content['device_id'])
            return self
        except ResponseError as e:
            try:
                reply = e.headers[u'WWW-Authenticate']
            except:
                raise e
        return reply
