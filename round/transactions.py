# -*- coding: utf-8 -*-
# transactions.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals
import logging

from .config import *

from .wrappers import *

logger = logging.getLogger(__name__)


class Transactions(ListWrapper):

    def wrap(self, resource):
        return Transaction(resource, self.client)


class Transaction(Wrapper):

    @property
    def attributes(self):
        return self.resource.attributes

    def __getattr__(self, name):
        try:
            return self.resource.attributes[name]
        except:
            return super(Transaction, self).__getattr__(name)

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
            logger.debug(e)
