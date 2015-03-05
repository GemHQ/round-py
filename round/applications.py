# -*- coding: utf-8 -*-
# applications.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
from .subscriptions import Subscriptions
import users


class Applications(DictWrapper):

    def create(self, **content):
        resource = self.resource.create(content)
        if u'instance_id' in content:
            resource.context.authorize(u'Gem-Application',
                                       api_token=resource.api_token,
                                       instance_id=content[u'instance_id'])
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return Application(resource, self.client)


class Application(Wrapper, Updatable):

    @property
    def users(self):
        if not hasattr(self, u'_users'):
            users_resource = self.resource.users
            self._users = users.Users(users_resource,
                                      self.client)
        return self._users

    def authorize_instance(self, **content):
        if (not hasattr(self, u'_application_instance') or
            not self._application_instance):
            self._application_instance = self.resource.authorize_instance(content)
            if self._application_instance:
                self.context.authorize(u'Gem-Application',
                                       api_token=self.api_token,
                                       instance_id=self._instance_id)
        return self._application_instance

    def reset(self):
        self.resource = self.resource.reset()
        return self

    @property
    def subscriptions(self):
        """
        Fetch and return Subscriptions associated with this account.
        """
        if not hasattr(self, '_subscriptions'):
            subscriptions_resource = self.resource.subscriptions
            self._subscriptions = Subscriptions(
                subscriptions_resource, self.client)
        return self._subscriptions
