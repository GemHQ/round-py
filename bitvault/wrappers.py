
import bitvault

class Wrapper(object):
    def __init__(self, resource):
        self.resource = resource

    def __getattr__(self, name):
        # TODO: may want to limit the delegation to specific attrs.
        return getattr(self.resource, name)

class User(Wrapper):

    def applications(self, refresh=False):
        if refresh or not self._applications:
            wrapper = bitvault.collections.Applications(self.resource.applications)
            self._applications = wrapper
        else:
            self._applications
        return self.applications

class Application(Wrapper):

    def wallets(self, refresh=False):
        if refresh or not self._wallets:
            wrapper = bitvault.collections.Wallets(self.resource.wallets)
            self._wallets = wrapper
        else:
            self._wallets
        return self.applications

class Account(Wrapper):

    def addresses(self, refresh=False):
        pass

    def payments(self, refresh=False):
        pass

    def transactions(self, refresh=False):
        pass

