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



class Users(Collection):

    def __init__(self, resource):
        super(Users, self).__init__(resource)

    def create(self, **content):
        resource = self.resource.create(content)
        resource.context.set_basic(content['email'], content['password'])
        return self.wrap(resource)

    def wrap(self, resource):
        return wrappers.User(resource=resource)


class Applications(Collection):
    
    def create(**content):
        resource = self.resource.create(content)
        resource.context.set_token(content['api_token'])
        app = wrap(resource)
        self.add(app)
        return app

    def wrap(self, resource):
        return wrappers.Application(resource=resource)



