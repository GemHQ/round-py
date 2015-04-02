# -*- coding: utf-8 -*-
# applications.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions
import users


class Applications(DictWrapper):
    """A collection of Application objects"""

    def create(self, **kwargs):
        """Create a new Application.

        Args:
          **kwargs: Arbitrary keyword arguments, including:
          name (str): A name for the new Application.

        Returns:
           A round.Application object if successful.
        """
        resource = self.resource.create(kwargs)
        if u'instance_token' in kwargs:
            resource.context.authorize(u'Gem-Application',
                                       api_token=resource.api_token,
                                       instance_id=kwargs[u'instance_token'])
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return Application(resource, self.client)


class Application(Wrapper, Updatable):
    """Representation of a Gem integration.

    Attributes:
      users (round.Users): A collection of Users who have an active device
        authorization on this Application.
    """

    @property
    def users(self):
        if not hasattr(self, u'_users'):
            users_resource = self.resource.users
            self._users = users.Users(users_resource, self.client)
        return self._users

    def reset(self):
        """Resets the `api_token` for this Application. This will cause all
        subsequent requests using the old `api_token` to fail.

        Returns:
          The Application.
        """
        self.resource = self.resource.reset()
        return self

    @property
    def subscriptions(self):
        """Fetch and return Subscriptions associated with this account."""
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
