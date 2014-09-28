import round

url = u'http://localhost:8998'
#url = u'http://round.pandastrike.com'
client = round.client(url)

auth = round.authed_client(url=url, email="foo@bar.com", password="baz")

import time
current_milli_time = lambda: int(round(time.time()))

email = '{0}@gem.co'.format(current_milli_time())

# should we be using kwargs this way?
user = client.users.create(email=email, password='a password')
print user.applications
print user.applications.refresh()
