from patchboard import discover
from bitvault.client import Context
import coinop

import time
current_milli_time = lambda: int(round(time.time()))

pb = discover(u"http://localhost:8998/",
        {'default_context': Context()})
client = pb.spawn()
resources = client.resources
users = resources.users

email = "matthew-{0}@bitvault.io".format(current_milli_time())
content = {'email': email, 'password': 'horriblepassword'}
user = users.create(content)

client.context.set_basic(email, 'horriblepassword')
#user.applications().list()

application = user.applications().create({'name': 'bitcoins_r_us'})
print repr(application)
client.context.set_token(application.api_token())

print application.wallets().list()






