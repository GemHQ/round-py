# client.py
#
# Copyright 2014 BitVault.


from bitvault import wrappers


class Client(object):

    def __init__(self, pb_client):
        self.pb_client = pb_client
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.users = wrappers.Users(resource=self.resources.users)

    @property
    def application(self):
        if not hasattr(self, '_application'):
            au = self.context.application_url
            ar = self.resources.application(au).get()
            self._application = wrappers.Application(ar)
        return self._application

    @property
    def user(self):
        # TODO: test this actually works
        if not hasattr(self, '_user'):
            email = self.context.email
            user_resource = self.resources.login({'email': email}).get()
            self._user = wrappers.User(user_resource)
        return self._user

    def wallet(self, url):
        # Not memoizing here, because a wallet is not a fundamental
        # part of a session, as a user or app would be.  Ditto account,
        # below.
        wallet_resource = self.resources.wallet(url).get()
        return wrappers.Wallet(wallet_resource)

    def account(self, url):
        account_resource = self.resources.account(url)
        return wrappers.Account(account_resource)
