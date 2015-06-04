# -*- coding: utf-8 -*-
# developers.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import *
import round.applications as apps


class Developers(object):

    def __init__(self, resource, client):
        self.resource = resource
        self.context = client.context
        self.client = client

    def create(self, **kwargs):

        resource = self.resource.create(kwargs)
        return self.wrap(resource)

    def wrap(self, resource):
        return Developer(resource, self.client)


class Developer(Wrapper):

    def update(self, phone_number):
        resource = self.resource.update({'phone_number': phone_number})

        return Developer(resource, self.client)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            apps_resource = self.resource.applications
            self._applications = apps.Applications(apps_resource,
                                                   self.client)
        return self._applications
