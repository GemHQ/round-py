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

    def get_applications(self, page=0, fetch=True):
        """Fetch and return the specified page of Applications owned by this
        Developer.
        """
        return apps.Applications(
            self.resource.applications, self.client, page, populate=fetch)

    @property
    @cacheable
    def applications(self):
        """Return the cached first page of Applications owned by this
        Developer.
        """
        return self.get_applications()
