# -*- coding: utf-8 -*-
# addresses.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import ListWrapper

class Addresses(ListWrapper):

    def __init__(self, resource, client, page=0, populate=True):
        super(Addresses, self).__init__(
            resource, client, page, populate=populate)

    def wrap(self, address):
        return address

    def create(self):
        address = self.resource.create()
        if len(self) < PAGE_LIMIT:
            self.add(address)
        return address
