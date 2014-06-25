# client.py
#
# Copyright 2014 BitVault.


from bitvault import collections


class Client(object):

    def __init__(self, pb_client):
        self.pb_client = pb_client
        self.context = self.pb_client.context
        self.resources = self.pb_client.resources
        self.users = collections.Users(resource=self.resources.users)
