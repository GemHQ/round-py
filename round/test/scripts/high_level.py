import round

url = u'https://api-develop.gem.co'
#url = u'http://round.pandastrike.com'
client = round.client(url)

auth = round.authed_client(url=url, email="foo@bar.com", password="baz")

import time
current_milli_time = lambda: int(round(time.time()))

email = '{0}@gem.co'.format(current_milli_time())

# should we be using kwargs this way?
developer = client.developers.create(email=email, password='a password')
print developer.applications
print developer.applications.refresh()
