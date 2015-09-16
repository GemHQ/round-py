# -*- coding: utf-8 -*-
# networks.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .wrappers import DictWrapper, Wrapper

class Networks(DictWrapper):

    def __init__(self, resource, client, populate=False):
        super(Networks, self).__init__(resource, client, populate=populate)

    def wrap(self, network):
        return Network(network, self.client)

    def key_for(self, network):
        return network.resource.name


class Network(Wrapper):

    @property
    def current_fee(self):
        return self.recommended_fee_per_kb
