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
          callback_url: URI of an active endpoint which can receive notifications

        Returns:
           A round.Subscription object if successful.
        """
        resource = self.resource.create({u'subscribed_to': u'address',
                                         u'callback_url': callback_url})
        subscription = self.wrap(resource)
        self.add(subscription)
        return subscription

    def add(self, subscription):
        """Add a Subscription to this collection.

        Args:
          subscription (round.Subscription)
        """
        self.data.append(subscription)

    def wrap(self, resource):
        """Construct a Subscription object from a server-side resource.

        Args:
          resource (patchboard.Resource)
        """
        return Subscription(resource, self.client)


class Subscription(Wrapper, Updatable):
    """A Subscription represents interest in any events on bitcoin addresses
    related to the Subscription's parent object.

    __init__ wraps an existing patchboard object that correlates to a server-side
    Subscription.

    Args:
      resource (patchboard.Resource)
      client (round.Client)
    """

    def __init__(self, resource, client):
        super(Subscription, self).__init__(resource, client)
