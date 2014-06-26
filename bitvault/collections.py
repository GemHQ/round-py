# collections.py
#
# Copyright 2014 BitVault.


from coinop.crypto.passphrasebox import PassphraseBox
from coinop.bit.multiwallet import MultiWallet

from bitvault import wrappers


class Collection(object):

    def __init__(self, resource):
        self.resource = resource
        self.collection = {}
        self.populate()

    def populate(self):
        if hasattr(self.resource, 'list'):
            resources = self.resource.list()
            for resource in resources:
                wrapper = self.wrap(resource)
                self.add(wrapper)

    def refresh(self):
        self.collection = {}
        self.populate()
        return(self)

    def add(self, wrapper):
        key = self.key_for(wrapper)
        self.collection[key] = wrapper

    def key_for(self, wrapper):
        return wrapper.name

    def find(self, key):
        return self.collection.get(key, None)

class Users(Collection):

    def __init__(self, resource):
        super(Users, self).__init__(resource)

    def create(self, **content):
        resource = self.resource.create(content)
        resource.context.set_user(content[u'email'], content[u'password'])
        return self.wrap(resource)

    def wrap(self, resource):
        return wrappers.User(resource=resource)


class Applications(Collection):

    def create(self, **content):
        resource = self.resource.create(content)
        resource.context.set_application(url=resource.url, token=resource.api_token)
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Application(resource=resource)


class Wallets(Collection):

    # The passphrase parameter should stay out of the content dict
    # so that there is no chance the client's passphrase will get passed
    # to our server.
    def create(self, passphrase, **content):
        multi_wallet = MultiWallet.generate([u"primary", u"backup"])
        primary_seed = multi_wallet.private_seed(u"primary")
        primary_public_seed = multi_wallet.public_seed(u'primary')
        backup_public_seed = multi_wallet.public_seed(u'backup')

        encrypted_seed = PassphraseBox.encrypt(passphrase, primary_seed)

        content[u'network'] = u'bitcoin_testnet'
        content[u'backup_public_seed'] = backup_public_seed
        content[u'primary_public_seed'] = primary_public_seed
        content[u'primary_private_seed'] = encrypted_seed

        resource = self.resource.create(content)
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Wallet(resource=resource)


class Accounts(Collection):

    def __init__(self, resource, wallet):
        self.wallet = wallet
        super(Accounts, self).__init__(resource)

    def create(self, **content):
        resource = self.resource.create(content)
        app = self.wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Account(resource=resource, wallet=self.wallet)

class Transactions(Collection):

    def __init__(self, resource):
        self.collection_list = []
        super(Transactions, self).__init__(resource)

    def add(self, wrapper):
        self.collection_list.append(wrapper)

    def wrap(self, resource):
        return wrappers.Transaction(resource=resource)


