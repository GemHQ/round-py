# -*- coding: utf-8 -*-
# users.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
import applications as apps
import wallets

class Users(DictWrapper):

    def create(self, email, **kwargs):
        backup_seed = None

        if u'passphrase' not in kwargs and u'wallet' not in kwargs:
            raise ValueError("Usage: users.create(email, passphrase='new-wallet-passphrase')")
        elif u'passphrase' in kwargs:
            backup_seed, wallet_data = wallets.generate(kwargs[u'passphrase'])
            del kwargs[u'passphrase']
            kwargs[u'wallet'] = wallet_data

        kwargs.update({u'email': email})

        resource = self.resource.create(kwargs)
        user = self.wrap(resource)
        self.add(user)
        return backup_seed, user

    def wrap(self, resource):
        return User(resource, self.client)

    def key_for(self, wrapper):
        return wrapper.email


class User(Wrapper, Updatable):

    def update(self, **content):
        resource = self.resource.update(content)
        return User(resource, self.client)

    @property
    def wallets(self):
        if not hasattr(self, '_wallets'):
            wallets_resource = self.resource.wallets
            self._wallets = wallets.Wallets(wallets_resource,
                                            self.client)
        return self._wallets

    def begin_device_authorization(self, name, device_id, api_token):
        try:
            self.context.schemes[u'Gem-OOB-OTP'][u'credential'] = 'api_token="{}"'.format(api_token)
            reply = self.resource.authorize_device({u'name': name,
                                                    u'device_id': device_id})
        except ResponseError as e:
            try:
                key = e.headers['WWW-Authenticate']['Gem-OOB-OTP'][u'key']
                self.current_otp_key = key
                return key
            except KeyError:
                raise OTPConflictError()
            except:
                raise e

    def complete_device_authorization(self, name, device_id, api_token, key, secret):
        try:
            self.client.authenticate_otp(api_token=api_token,
                                         key=key, secret=secret)

            r = self.resource.authorize_device({u'name': name,
                                                u'device_id': device_id})

        except ResponseError as e:
            try:
                new_key = e.headers['WWW-Authenticate']['Gem-OOB-OTP'][u'key']
                if new_key == key:
                    raise e
                else:
                    raise UnknownKeyError(new_key)
            except KeyError:
                raise e

        self.client.authenticate_device(api_token=api_token,
                                        user_url=r.url,
                                        user_token=r.user_token,
                                        device_id=device_id,
                                        override=True)

        return User(r, self.client)
