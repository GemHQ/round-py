# -*- coding: utf-8 -*-
# developers.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
import applications as apps


class Developers(object):

    def __init__(self, resource, client):
        self.resource = resource
        self.context = client.context
        self.client = client

    def create(self, **content):
        priv = content[u'privkey'] if u'privkey' in content else None
        resource = self.resource.create(content)
        if priv:
            resource.context.authorize(u'Gem-Developer',
                                       email=content[u'email'],
                                       privkey=priv)
        return self.wrap(resource)

    def wrap(self, resource):
        return Developer(resource, self.client)


class Developer(Wrapper):

    def update(self, **content):
        resource = self.resource.update(content)

        email = resource.attributes.get(u'email', None)
        priv = content.get(u'privkey', None)

        resource.context.authorize(u'Gem-Developer',
                                   email=email,
                                   privkey=priv)
        return Developer(resource, self.client)

    @property
    def applications(self):
        if not hasattr(self, '_applications'):
            apps_resource = self.resource.applications
            self._applications = apps.Applications(apps_resource,
                                                   self.client)
        return self._applications
