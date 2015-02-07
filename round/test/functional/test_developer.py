# test_developer.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
import time
import patchboard
import round

pubkey = u'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoVw+yyLfmMRSuQcUAQFK\n7I4hLYXnpt23Avl/jmHqH50HU4PiOUKSBqwoCzu6jgOzZMcZoZV5Hor86czaASqN\nJPjSVnJDmh7nav2S6IzZ7nbXI/OT26JZgtr1jieaH++o2+aV47u/tK1wPyGPM+8D\n8XpojxPOgoihNg8kXRwng6SAmqXp94Kny019qvyvjJkvM+PxehhrS1s3jv59d7NF\nbYRZlTkj9ZfXlacVcK70LfdCrdUfU2AFB4v4zHnPoEO7jGCODtXAi7PlR/nVLD36\nMGy548ozpiYI0yyM3+sJCig4W+GPifWUNtyrASUyU7u1frZ56QELJgJ+NFsBsR9l\nhQIDAQAB\n-----END PUBLIC KEY-----\n'
privkey = u'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAoVw+yyLfmMRSuQcUAQFK7I4hLYXnpt23Avl/jmHqH50HU4Pi\nOUKSBqwoCzu6jgOzZMcZoZV5Hor86czaASqNJPjSVnJDmh7nav2S6IzZ7nbXI/OT\n26JZgtr1jieaH++o2+aV47u/tK1wPyGPM+8D8XpojxPOgoihNg8kXRwng6SAmqXp\n94Kny019qvyvjJkvM+PxehhrS1s3jv59d7NFbYRZlTkj9ZfXlacVcK70LfdCrdUf\nU2AFB4v4zHnPoEO7jGCODtXAi7PlR/nVLD36MGy548ozpiYI0yyM3+sJCig4W+GP\nifWUNtyrASUyU7u1frZ56QELJgJ+NFsBsR9lhQIDAQABAoIBABRVDUyHbmlPg6Tw\n8WJXCVvZZPDZiKEMGv1y9tG4IMou/TdWzPCuJLxWgQ05T36JlNdEB0THEuX4WXoU\nZ/vxoqtf9xERgNcwwbRHk3VeGi/kJaPQE3d/c4v7jymEb/VKO5rJ6WUyySs5F4W8\n8tB2c6a/5+Dve/wSv02ShuB8pbX+lzF3Rh7VPHjonXxFWiS5FtehK/OFAmHXUTrQ\n0DlXBA2R437vVnmFORJE8HNpHabD8eYa8aoLBY7Yz8qWYxfrwde43r19rJkitS5B\neU5lGt6os4UinZ+JnfXKFjKbfb7ZAuRj3rkR+TgPvoRADyR4XKqs6fgohZzlC0Is\nP0bz15kCgYEA1siFjGtvgLowio7fM0SWadfykg1kSPa0vpPencXFtBBNaJDbz0F/\nB2kRp3TWw6g8hhBKZlWrfsFQa4R+pEbh/bRc6Edkh64VGWMNJ/2NxYAy+eB6DVl/\nFlLGI669MruPjoGe5aNTj03LoddGXS/04TyvNcDaK52KAw629+Glto8CgYEAwFNC\nSuG3qVNLv2+alvBtjJs+s0oznDJ/USwqYbSOOtr0EmjnTN1mDCT1EvTKNN24e/KE\ntzlzzvFnjWx+bysKg6Q4xIUmof5Q6f8hY/bASWdjaKjJxWNOTVnFtL/KMQDTA5X5\naBbZATB2FCNH0Xce5YYeL7m2uK1HT1ZDtOUETKsCgYEAtcz7hdU2h36SMeYnNW0b\n6DF6yHd/aGcyrJHbgC50Xyrhat4awL7OuEYORHEYjHqt6EiHwUFIrT0SRj/bNlAt\nYCM39QDhLhuDDn8SFsR/KSqPe4SvqvcTJKEhx/hTe0rZg6ViCzyJMSaHc9EVZTF/\nlNtZ7yTzRrHNrTLaWs1sCC8CgYA36z1YJl7PNa/NfnaVMly3yB+n44gz/x6zjELa\nW7QK+sSCYcv2tlzIZSp4k4IDcwAD0dSyrVq1rczs+sGcMwiAlAwJX6mG6jm+f3bG\n6OSpswzdTk40PRZ0OQjZ7/Wq39F6tm1ozVPVG7EJU+S6y4bJN4CpYbb15TPZpnxT\nKU9htwKBgDXiGEX56CbIw0O1AFfYEDCjDzG9HPcOtFjxvSLcIrBb1Yl+Tov3zgrZ\ns4HPVSGyi1d2T/ytIT0qWocrdO2YY3F9FhluzXrOcKlVBEGbyItx6gUCmepmp1dR\ndadVrwjj3IYw6Wa3z5+vzxviy3yCq/68yq5A+5mrAHF3Z1ZSDg4U\n-----END RSA PRIVATE KEY-----\n'

api_token = 'ssgPhVv-Pv-soqQtRM7pIFHzg7uGOGFzrAfSBVONqgo'
user_token = '0x20mNTVcUWujHrtGENR9NjSF0_K6JYLlDfMTMUjh-Q'
device_id = 'joshua+userJava06@gem.codevice6'
user_url = 'https://api-sandbox.gem.co/users/1bIKvHKszboJhLBr2PfLLA'
email = 'joshua+userJava06@gem.co'
instance_id = u'DE73gGgLcJB07D0gW0G3VUN3aywgcd1T8F3bT-0eTy8'
app_url = u'https://api-sandbox.gem.co/apps/oHgM6NrHq-C_K2-f1pfwIg'
dev_email= u'joshua+devJava1@gem.co'
random_instance_name = instance_name()
create = False

print random_instance_name

c = round.client()

class TestDeveloper:
	def test_developer_functionality(self):
			dev = c.authenticate_developer(email=dev_email, privkey=privkey)
			
			app = dev.applications['default']
			assert app.api_token == api_token

			#test creation of an application		
			if create:
				num_apps = len(dev.applications)
				new_app = dev.applications.create(name=app_name())
				assert isinstance(new_app.api_token, basestring)
				assert new_app.api_token != api_token
				assert len(dev.refresh().applications) > num_apps

	def test_authorize_new_instance(self):
			if create:
				dev = c.authenticate_developer(email=dev_email, privkey=privkey, override = True)
				app = dev.applications['default']
				ai = app.authorize_instance(name=random_instance_name)

				assert  ai.name == random_instance_name

	def test_instance_authentication(self):
			app = c.authenticate_application(app_url=app_url, 
                                          api_token=api_token, 
                                          instance_id=instance_id)
			assert len(app.users) > 0

			for u in app.users.itervalues():
				for w in u.wallets.itervalues():
					assert w.balance >= 0

			dev = c.authenticate_developer(email=dev_email, privkey=privkey, override = True)
			assert app.name == dev.applications['default'].name

	def test_app_instance_data_access(self):
			app = c.authenticate_application(app_url=app_url, 
                                          api_token=api_token, 
                                          instance_id=instance_id,
                                          override = True)
			# in app auth test you can get info about a user
			# wallet and the account but fail on creation
			u = app.users[email]
			with raises(round.AuthenticationError):
				u.wallets.create(name='wallet', passphrase='password')	
			assert u.user_token == user_token
			assert len(u.wallets) > 1

			w = u.wallets['default']
			with raises(round.AuthenticationError):
				w.accounts.create(name='blah')
			assert isinstance(w.balance, int)
			assert w.name == 'default'

			a = w.accounts['newChecking']
			with raises(round.AuthenticationError):
				a.addresses.create()
			with raises(round.AuthenticationError):
				a.pay([{'address':'mu8fvJkPpBxaNpLB2vF17nX2iHYZcHb15h', 'amount': 20000}])
			assert isinstance(a.balance, int)
			assert isinstance(a.pending_balance, int)

			txs = a.transactions()
			assert len(txs) > 0
			assert isinstance(txs[2].data['hash'],unicode)




			

