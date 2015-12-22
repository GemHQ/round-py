# -*- coding: utf-8 -*-
# networks.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

from .config import *

from .assets import AssetTypes
from .wrappers import *

class Networks(DictWrapper):

    def __init__(self, resource, client, page=0, populate=False):
        super(Networks, self).__init__(resource, client,
                                       page=page, populate=populate)

    def wrap(self, network):
        return Network(network, self.client)

    def key_for(self, network):
        return network.resource.name


class Network(Wrapper):

    @property
    def current_fee(self):
        return self.recommended_fee_per_kb

    @property
    @cacheable
    def asset_types(self):
        """
        Fetch and return an updted list of AssetTypes currently on this network.
        """
        return self.get_asset_types()

    def get_asset_types(self, page=0, fetch=False):
        """
        Return the Network's asset_types object, populating it if fetch is True.
        """
        return AssetTypes(self.resource.asset_types, self.client,
                         page=page, populate=fetch)
