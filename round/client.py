# -*- coding: utf-8 -*-
# client.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from round import wrappers


class Client(object):

    def __init__(self, pb_client):
        self.pb_client = pb_client
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.developers = wrappers.Developers(resource=self.resources.developers)

    @property
    def application(self):
        if not hasattr(self, '_application'):
            au = self.context.application_url
            ar = self.resources.application(au).get()
            self._application = wrappers.Application(ar)
        return self._application

    @property
    def developer(self):
        if not hasattr(self, '_developer'):
            try:
                dev_resource = self.resources.developers.get()
                self._developer = wrappers.Developer(dev_resource)
            except Exception as e:
                raise Exception(u"Must call client.context.set_developer(email, password) first")

        return self._developer

    def wallet(self, url):
        # Not memoizing here, because a wallet is not a fundamental
        # part of a session, as a user or app would be.  Ditto account,
        # below.
        wallet_resource = self.resources.wallet(url).get()
        return wrappers.Wallet(wallet_resource)

    def account(self, url):
        account_resource = self.resources.account(url)
        return wrappers.Account(account_resource)
