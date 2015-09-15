# -*- coding: utf-8 -*-
# addresses.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import ListWrapper

class Addresses(ListWrapper):

    def __init__(self, resource, client, populate=False):
        super(Addresses, self).__init__(resource, client, populate)

    def wrap(self, address):
        return address

    def create(self):
        address = self.resource.create()
        self.add(address)
        return address
