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

    def add(self, wrapper):
        key = self.key_for(wrapper)
        self.collection[key] = wrapper

    def key_for(self, wrapper):
        return wrapper.name



class Users(Collection):

    def __init__(self, resource):
        super(Users, self).__init__(resource)

    def create(self, **content):
        return self.wrap(self.resource.create(content))

    def wrap(self, resource):
        return wrappers.User(resource=resource)

class Applications(Collection):
    
    def create(**content):
        app = wrap(self.resource.create(content))
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Application(resource=resource)



