from patchboard import discover
import coinop

import time
current_milli_time = lambda: int(round(time.time() * 1000))

class Context(dict):

    def authorizer(self, *args):
        raise Exception("unimplemented")


def test_foo():
    pb = discover(u"http://localhost:8998/",
            {'default_context': lambda: Context()})
    client = pb.spawn()
    users = client.resources.users
    email = "matthew-{0}@bitvault.io".format(current_milli_time())
    content = {'email': email, 'password': 'horriblepassword'}
    user = users.create(content)



