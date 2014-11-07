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

    def begin_device_authorization(self, name, device_id):
        try:
            del self.context.schemes[u'Gem-OOB-OTP']['credential']
            self.current_device_name = name
            self.current_device_id = device_id
            reply = self.resource.authorize_device(name=name, device_id=device_id)
        except ResponseError as e:
            try:
                reply = {'message': 'Device authorization requested'}
                self.current_otp_key = reply['Gem-OOB-OTP']['key']
            return self
            except:
                raise e
        return reply

    def complete_device_authorization(self, app_url, api_token, secret):
        try:
            self.client.authenticate_otp(api_token=api_token,
                                         key=self.current_otp_key,
                                         secret=secret)

            r = self.resource.authorize_device(name=self.current_device_name,
                                               device_id=self.current_device_id)

            self.client.authenticate_device(app_url=app_url,
                                            api_token=api_token,
                                            user_url=r.url,
                                            user_token=r.user_token,
                                            device_id=self.current_device_id)
            return User(r, self.client)
