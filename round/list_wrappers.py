# -*- coding: utf-8 -*-
# collections.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import collections

import wrappers


class ListWrapper(collections.Sequence):

    def __init__(self, resource):
        self.resource = resource
        self.data = []
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __len__(self):
        return self.data.__len__()

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


class Transactions(ListWrapper):

    def __init__(self, resource):
        self.collection_list = []
        super(Transactions, self).__init__(resource)

    def add(self, wrapper):
        self.collection_list.append(wrapper)

    def wrap(self, resource):
        return wrappers.Transaction(resource=resource)


class Addresses(ListWrapper):

    def __init__(self, resource):
        self.collection_list = []
        super(Addresses, self).__init__(resource)

    def add(self, address):
        self.collection_list.append(address)

    def wrap(self, address):
        return address

    def create(self):
        address = self.resource.create()
        self.add(address)
        return address
