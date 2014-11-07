# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
import applications as apps
import wallets

class Users(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        user = self.wrap(resource)
        self.add(user)
        return user

    def wrap(self, resource):
        return User(resource, self.client)

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
            self._applications = apps.Applications(apps_resource,
                                                   self.client)
        return self._applications

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = wallets.Wallets(wallets_resource,
                                            self.client)
        return self._wallets

    def authorize_device(self, **content):
        try:
            reply = self.resource.authorize_device(content)
            # Doesn't require the app_url, since that is only for the
            # client.application convenience method.
            appurl = self.context.app_url if hasattr(self.context, 'app_url') else None
            self.client.authenticate_device(
                api_token=self.context.api_token,
                user_url=self.url,
                user_token=self.user_token,
                device_id=content['device_id'],
                app_url=appurl)
            return self
        except ResponseError as e:
            try:
                reply = e.headers[u'WWW-Authenticate']
            except:
                raise e
        return reply
