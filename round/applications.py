# -*- coding: utf-8 -*-
# applications.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from .config import *

from .wrappers import *
import users
import rules


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

    @property
    def rules(self):
        if not hasattr(self, u'_rules'):
            rules_resource = self.resource.rules
            self._rules = rules.Rules(rules_resource,
                                      self.client)
        return self._rules

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