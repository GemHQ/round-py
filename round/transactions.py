# -*- coding: utf-8 -*-
# transactions.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import *


class Transactions(ListWrapper):

    def __init__(self, resource, client, page=0, populate=True, **query):
        self._data = []
        super(ListWrapper, self).__init__(resource, client, page,
                                          populate=populate, **query)

    def wrap(self, resource):
        return Transaction(resource, self.client)


class Transaction(Wrapper):

    def approve(self, mfa_token=None):
        if mfa_token:
            return self.with_mfa(mfa_token).resource.approve({})

        return self.resource.approve({})

    @property
    def mfa_uri(self):
        try:
            return self.resource.__dict__['mfa_uri']
        except KeyError:
            pass
        try:
            return self.resource.__dict__['attributes']['mfa_uri']
        except KeyError:
            pass
        return None

    def cancel(self):
        try:
            return self.resource.cancel()
        except Exception as e:
            print(e)
