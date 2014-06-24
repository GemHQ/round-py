import bitvault

client = bitvault.client("http://localhost:8998/")

auth = bitvault.authed_client(url="http://localhost:8998",
        email="foo@bar.com", password="baz")

import time
current_milli_time = lambda: int(round(time.time()))

email = '{0}@bitvault.io'.format(current_milli_time())

print client.users.create(email=email, password='a password')

