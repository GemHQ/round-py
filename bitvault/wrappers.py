
import bitvault

class Wrapper(object):
    def __init__(self, resource):
        self.resource = resource

    def __getattr__(self, name):
        # TODO: may want to limit the delegation to specific attrs.
        return getattr(self.resource, name)

class User(Wrapper):

    def __init__(self, resource):
        super(User, self).__init__(resource)
        app_resource = self.resource.applications
        self.applications = bitvault.collections.Applications(app_resource)


class Application(Wrapper):

    def wallets(self):
        pass

class Account(Wrapper):

    def addresses(self, refresh=False):
        pass

    def payments(self, refresh=False):
        pass

    def transactions(self, refresh=False):
        pass

