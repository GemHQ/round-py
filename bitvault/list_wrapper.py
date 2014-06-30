# collections.py
#
# Copyright 2014 BitVault.


import abc
import collections as monkey

print dir(monkey)
exit()

from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

from bitvault import wrappers

class DictWrapper(collections.Mapping):

    def __init__(self, resource):
        self.resource = resource
        self.data = {}
        self.populate()

    def __getitem__(self, name):
        return data.__getitem__(name)

    def __iter__(self):
        pass

    def __len__(self):
        return data.__len__()

    def populate(self):
        if hasattr(self.resource, 'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                key = self.key_for(wrapper)
                self.collection[key] = wrapper


    def refresh(self):
        self.data = {}
        self.populate()
        return(self)

    @abc.abstractmethod
    def key_for(self, wrapper):
        return wrapper.name



class Transactions(ListWrapper):

    def __init__(self, resource):
        self.collection_list = []
        super(Transactions, self).__init__(resource)

    def add(self, wrapper):
        self.collection_list.append(wrapper)

    def wrap(self, resource):
        return wrappers.Transaction(resource=resource)



