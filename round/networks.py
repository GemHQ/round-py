# -*- coding: utf-8 -*-
# networks.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import ListWrapper, Wrapper

class Networks(ListWrapper):

    def __init__(self, resource, client, populate=False):
        super(Networks, self).__init__(resource, client, populate)

    def wrap(self, network):
        return Network(network, self.client)

class Network(Wrapper):

    def __repr__(self):
        return repr(self.attributes)

    def current_fee(self):
        return self.recommended_fee_per_kb
