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

    def begin_device_authorization(self, name, device_id, api_token=None):
        try:
            self.current_api_token = api_token if api_token else self.context.api_token
            self.context.schemes[u'Gem-OOB-OTP'][u'credential'] = 'api_token="{}"'.format(
                self.current_api_token)
            self.current_device_name = name
            self.current_device_id = device_id
            reply = self.resource.authorize_device({u'name': name,
                                                    u'device_id': device_id})
        except AttributeError:
            raise Exception("No api_token found on client. You must supply an api_token parameter.")
        except ResponseError as e:
            try:
                key = e.headers['WWW-Authenticate']['Gem-OOB-OTP'][u'key']
                self.current_otp_key = key
                return key
            except:
                raise e

    def complete_device_authorization(self, secret, name=None, device_id=None, api_token=None, key=None, app_url=None):
        try:
            # Ugly
            key = key if key else self.current_otp_key
            name = name if name else self.current_device_name
            device_id = device_id if device_id else self.current_device_id
            api_token = api_token if api_token else (self.current_api_token if hasattr(self, 'current_api_token') else self.context.api_token)
            self.client.authenticate_otp(api_token=api_token,
                                         key=key, secret=secret)

            r = self.resource.authorize_device({u'name': name,
                                                u'device_id': device_id})

        except AttributeError:
            raise Exception("You must first call user.begin_device_authorization(name='name', device_id='device_id', api_token='api_token')")

        try:
            app_url = app_url if app_url else self.context.app_url
            self.client.authenticate_device(app_url=app_url,
                                            api_token=api_token,
                                            user_url=r.url,
                                            user_token=r.user_token,
                                            device_id=device_id)
        except AttributeError:
            print "Warning: Device authorized successfully, but user not authenticated, use `user.client.authenticate_device`"

        return User(r, self.client)
