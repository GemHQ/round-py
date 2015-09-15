# -*- coding: utf-8 -*-
# transactions.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals
import logging

from .config import *

from .wrappers import *

logger = logging.getLogger(__name__)


class NetkiDomains(ListWrapper):

    def wrap(self, resource):
        return NetkiDomain(resource, self.client)

    def create(self, domain_name, partner_id=None):
        """Register a domain you control with netki as a Gem-managed domain.
        Note: After registering a domain, unless you have already set up its
        DNSSEC/DS Records, you'll need to do so: http://docs.netki.apiary.io
        The information required will be an attribute of the returned NetkiDomain
        object.

        Args:
          domain_name (str): Domain to add (e.g. 'gem.co')
          partner_id (str, optional): your netki partner_id (if you have one)

        Returns: The new round.NetkiDomain
        """
        params = dict(domain_name=domain_name)

        if partner_id: params['partner_id'] = partner_id

        domain = self.wrap(self.resource.create(params))

        self.add(domain)
        return domain


class NetkiDomain(Wrapper):
    pass


class NetkiNames(ListWrapper):

    def wrap(self, resource):
        return NetkiName(resource, self.client)

    def create(self, name, domain_name):
        """Register a url (e.g. wallet.gem.co) for

        Args:
          name (str): human-readable wallet name (e.g. wallet)
          domain_name (str): the domain name to create subdomain on (e.g. gem.co)
            this domain must already be registered with Gem

        Returns: The new round.NetkiName
        """
        name = self.wrap(self.resource.create(dict(name=name,
                                                   domain_name=domain_name)))

        self.add(name)
        return name


class NetkiName(Wrapper):
    pass
