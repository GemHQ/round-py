# -*- coding: utf-8 -*-
# transactions.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *


class Transactions(ListWrapper):

    def __init__(self, resource, client):
        self.collection_list = []
        super(Transactions, self).__init__(resource, client)

    def add(self, wrapper):
        self.collection_list.append(wrapper)

    def wrap(self, resource):
        return Transaction(resource, self.client)


class Transaction(Wrapper):

    @property
    def attributes(self):
        return self.resource.attributes

    def approve(self, mfa_token=None):
        if mfa_token:
            return self.with_mfa(mfa_token).resource.approve({})

        return self.resource.approve({})

    def cancel(self):
        try:
            return self.resource.cancel()
        except Exception as e:
            print(e)
