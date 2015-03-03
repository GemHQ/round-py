# -*- coding: utf-8 -*-
# wallets.py
#
# Copyright 2015 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *

class Subscriptions(ListWrapper):

    def create(self, callback_url):
        """
        Create a new Subscription on all addresses contained by this collection's
        parent object.
        Return the new round.Subscription object.
        Keyword arguments:
        callback_url -- URI of an active endpoint which can receive notifications
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

    def __init__(self, resource, client):
        """
        Initialize a round.Subscription from an Account patchboard.Resource object.
        Keyword arguments:
        resource --  Subscription patchboard.Resource object
        client -- authenticated round.Client object
        """
        super(Subscription, self).__init__(resource, client)
