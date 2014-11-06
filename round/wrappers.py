# -*- coding: utf-8 -*-
# wrappers.py
#
# Copyright 2014 BitVault, Inc. dba Gem

import abc
import collections

from .config import *

from coinop.bit.transaction import Transaction as Tx

from patchboard.response import ResponseError

from pprint import pprint as pp

class Updatable(object):

    def update(self, **content):
        return self.__class__(self.resource.update(content),
                              self.client)


class Wrapper(object):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client

    def __getattr__(self, name):
        return getattr(self.resource, name)

    def __str__(self):
        return str(self.attributes)

    def refresh(self):
        self.resource = self.resource.get()
        return self


class DictWrapper(collections.Mapping):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client
        self.data = {}
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return repr(self.items())

    def populate(self):
        if hasattr(self.resource, u'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.add(wrapper)

    def add(self, wrapper):
        key = self.key_for(wrapper)
        self.data[key] = wrapper

    def refresh(self):
        self.data = {}
        self.populate()
        return(self)

    def key_for(self, wrapper):
        return wrapper.name

    @abc.abstractmethod
    def wrap(self, resource):
        pass


class ListWrapper(collections.Sequence):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client
        self.data = []
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return repr(self.data)

    def populate(self):
        if hasattr(self.resource, u'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.data.append(wrapper)

    def refresh(self):
        self.data = []
        self.populate()
        return(self)
