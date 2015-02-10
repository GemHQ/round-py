# -*- coding: utf-8 -*-
# rules.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import collections

from .config import *

from .wrappers import *


class Rules(collections.Mapping):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client
        self.refresh()

    def __getitem__(self, name):
        return self.definitions.__getitem__(name)

    def __iter__(self):
        return self.definitions.__iter__()

    def __len__(self):
        return self.definitions.__len__()

    def refresh(self):
        self.cache = self.resource.get()
        self.definitions = {}
        for key, value in self.cache.definitions.iteritems():
            self.definitions[key] = self.wrap(value)
        return self

    def wrap(self, resource):
        return Rule(resource, self.client)

    def add(self, name):
        return self.wrap(self.resource.add(dict(name=name)))


class Rule(Wrapper):

    def set(self, content):
        for name, spec in content.iteritems():
            if spec[u'type'] in [u'wallet', u'account']:
                resource = spec[u'value']
                spec[u'value'] = dict(url=resource[u'url'])
        return self.resource.set(content)

    def delete(self):
        return self.resource.delete.response.data
