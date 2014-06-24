from bitvault import collections

class Client(object):

    def __init__(self, client):
        self.client = client
        self.context = self.client.context
        self.resources = self.client.resources
        self.users = collections.Users(resource=self.resources.users)



