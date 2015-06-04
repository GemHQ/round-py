# -*- coding: utf-8 -*-
# wrappers.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from __future__ import unicode_literals
from .config import *

from patchboard.response import ResponseError
from coinop.transaction import Transaction as Tx

import abc
import collections

from .errors import *


class Updatable(object):

    def update(self, **kwargs):
        return self.__class__(self.resource.update(kwargs), self.client)


class MFAable(object):

    def with_mfa(self, mfa_token):
        """Set the MFA token for the next request.
        `mfa_token`s are only good for one request. Use this method to chain into
        the protected action you want to perform.

        Note: Only useful for Application authentication.
        Usage:
          account.with_mfa(application.totp.now()).pay(...)

        Args:
          mfa_token (str): A valid TOTP mfa token derived from the `totp_secret`
            on an Application.

        Returns:
          self
        """
        self.context.mfa_token = mfa_token
        return self


class Wrapper(MFAable):

    def __init__(self, resource, client):
        self.resource = resource
        self.context = client.context
        self.client = client

    def __getattr__(self, name):
        try:
            return getattr(self.resource, name)
        except ResponseError as e:
            raise RoundError(e.message)

    def __str__(self):
        return str(self.attributes)

    def refresh(self):
        try:
            self.resource = self.resource.get()
        except ResponseError as e:
            raise RoundError(e.message)
        return self

class DictWrapper(collections.Mapping):

    def __init__(self, resource, client):
        self.resource = resource
        self.context = client.context
        self.client = client
        self.data = {}
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __iter__(self):
        return self.data.__iter__()

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return repr(self.data.items())

    def populate(self):
        if hasattr(self.resource, 'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.add(wrapper)

    def add(self, wrapper):
        key = self.key_for(wrapper)
        self.data[key] = wrapper
        return wrapper

    def refresh(self):
        self.data = {}
        self.populate()
        return(self)

    def with_mfa(self, mfa_token):
        self.context.mfa_token = mfa_token
        return self

    def key_for(self, wrapper):
        try:
            return wrapper.name
        except:
            return wrapper.key

    @abc.abstractmethod
    def wrap(self, resource):
        pass


class ListWrapper(collections.Sequence):

    def __init__(self, resource, client):
        self.resource = resource
        self.context = client.context
        self.client = client
        self.data = []
        self.populate()

    def __getitem__(self, name):
        return self.data.__getitem__(name)

    def __len__(self):
        return self.data.__len__()

    def __repr__(self):
        return repr(self.data)

    def populate(self):
        if hasattr(self.resource, 'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.data.append(wrapper)

    def refresh(self):
        self.data = []
        self.populate()
        return(self)

    def with_mfa(self, mfa_token):
        self.context.mfa_token = mfa_token
        return self
