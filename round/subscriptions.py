# -*- coding: utf-8 -*-
# wallets.py
#
# Copyright 2015 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *

class Subscriptions(ListWrapper):
    """A collection of Subscription objects"""

    def create(self, callback_url):
        """Register a new Subscription on this collection's parent object.

        Args:
          callback_url (str): URI of an active endpoint which can receive
          notifications.

        Returns:
           A round.Subscription object if successful.
        """
        resource = self.resource.create({u'subscribed_to': u'address',
                                         u'callback_url': callback_url})
        subscription = self.wrap(resource)
        self.add(subscription)
        return subscription

    def add(self, subscription):
        self.data.append(subscription)

    def wrap(self, resource):
        return Subscription(resource, self.client)


class Subscription(Wrapper, Updatable):
    """A Subscription represents interest in any events on bitcoin addresses
    related to the Subscription's parent object.
    """

    def __init__(self, resource, client):
        super(Subscription, self).__init__(resource, client)
