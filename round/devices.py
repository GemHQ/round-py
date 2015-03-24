# -*- coding: utf-8 -*-
# devices.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *

class Devices(DictWrapper):

    def create(self, name, device_id, api_token=None):
        try:
            self.client.authenticate_identify(api_token)
        except:
            pass

        resource = self.resource.create({u'name': name,
                                         u'device_id': device_id})
        device = self.wrap(resource)
        self.add(device)
        return device

    def wrap(self, resource):
        return Device(resource, self.client)


# TODO: Updatable device names? Possibly no.
# class Device(Wrapper, Updatable):
#     def update(self, name):
#         resource = self.resource.update({'name': name})
#         return Device(resource, self.client)

class Device(Wrapper):
    pass
