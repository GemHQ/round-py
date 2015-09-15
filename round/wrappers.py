# -*- coding: utf-8 -*-
#
# wrappers.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals
from functools import wraps
from .config import *

from patchboard.response import ResponseError
from coinop.transaction import Transaction as Tx

import abc
import collections

from .errors import *

def cacheable(func):
    @wraps(func)
    def func_wrapper(self):
        name = '_{}'.format(func.__name__)
        if not hasattr(self, name):
            setattr(self, name, func(self))
        return getattr(self, name)
    return func_wrapper


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
          mfa_token (str/function, optional): TOTP token for the Application
            OR a callable/function which will generate such a token when called.

        Returns:
          self
        """
        if hasattr(mfa_token, '__call__'): # callable() is unsupported by 3.1 and 3.2
            self.context.mfa_token = mfa_token.__call__()
        else:
            self.context.mfa_token = mfa_token
        return self


class Wrapper(MFAable):

    def __init__(self, resource, client):
        self.resource = resource
        self.client = client

    def __getattr__(self, name):
        # TODO: This is horrific and mostly due to the 'attributes' attribute in
        # patchboard. Normalize attribute access once patchboard dies in a fire.
        if name in self.__dict__:
            return self.__dict__[name]
        if name in self.resource.__dict__:
            return self.resource.__dict__[name]
        if name in self.resource.attributes:
            return self.resource.attributes[name]
        try:
            return getattr(self.resource, name)
        except ResponseError as e:
            raise RoundError(e.message)

    def __str__(self):
        return str(self.attributes)

    @property
    def context(self):
        return self.client.context

    def refresh(self):
        try:
            self.resource = self.resource.get()
        except ResponseError as e:
            raise RoundError(e.message)
        return self


class DictWrapper(MFAable, collections.Mapping):

    def __init__(self, resource, client, populate=False):
        self.resource = resource
        self.client = client
        self._data = {}
        self._populated = False
        if populate: self.populate()

    def __getitem__(self, name):
        if name not in self._data and not self._populated: self.populate()
        return self._data.__getitem__(name)

    def __iter__(self):
        self.populate()
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __repr__(self):
        self.populate()
        return repr(self._data.items())

    def populate(self, if_populated=False):
        if ( hasattr(self.resource, 'list') and
             (if_populated or not self._populated) ):
            for resource in self.resource.list():
                self.add(self.wrap(resource))
            self._populated = True

    def add(self, wrapper):
        self._data[self.key_for(wrapper)] = wrapper
        return wrapper

    def refresh(self):
        self._data = {}
        self.populate(True)
        return self

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

    def __init__(self, resource, client, populate=False):
        self.resource = resource
        self.client = client
        self._data = []
        self._populated = False
        if populate: self.populate()

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

    def __iter__(self):
        self.populate()
        return iter(self._data)

    def __repr__(self):
        self.populate()
        return repr(self._data)

    def add(self, value):
        self._data.append(value)
        return value

    def populate(self, if_populated=False):
        if ( hasattr(self.resource, 'list') and
             (if_populated or not self._populated) ):
            resources = self.resource.list()
            for resource in resources:
                self._data.append(self.wrap(resource))
            self._populated = True

    def refresh(self):
        self._data = []
        self.populate(True)
        return(self)

    def with_mfa(self, mfa_token):
        self.context.mfa_token = mfa_token
        return self

    @abc.abstractmethod
    def wrap(self, resource):
        pass
