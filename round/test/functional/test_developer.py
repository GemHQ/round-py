# test_developer.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
import time
import patchboard
import round

pubkey = open('roundKeys/pub.pem', 'r').read()
privkey = open('roundKeys/priv.pem', 'r').read()
api_token = 'ssgPhVv-Pv-soqQtRM7pIFHzg7uGOGFzrAfSBVONqgo'
user_token = '0x20mNTVcUWujHrtGENR9NjSF0_K6JYLlDfMTMUjh-Q'
device_id = 'joshua+userJava06@gem.codevice6'
user_url = 'https://api-sandbox.gem.co/users/1bIKvHKszboJhLBr2PfLLA'
email = 'joshua+userJava06@gem.co'
instance_id = u'DE73gGgLcJB07D0gW0G3VUN3aywgcd1T8F3bT-0eTy8'
app_url = u'https://api-sandbox.gem.co/apps/oHgM6NrHq-C_K2-f1pfwIg'
dev_email= u'joshua+devJava1@gem.co'
random_instance_name = instance_name()

print random_instance_name

c = round.client()

class TestDeveloper:
	def test_developer_functionality(self):
			dev = c.authenticate_developer(email=dev_email, privkey=privkey)
			
			app = dev.applications['default']
			assert app.api_token == api_token

			#test creation of an application
			create = False
			if create:
				num_apps = len(dev.applications)
				new_app = dev.applications.create(name=app_name())
				assert isinstance(new_app.api_token, basestring)
				assert new_app.api_token != api_token
				assert len(dev.refresh().applications) > num_apps

	def test_authorize_new_instance(self):
			create = False
			if create:
				dev = c.authenticate_developer(email=dev_email, privkey=privkey, override = True)
				app = dev.applications['default']
				ai = app.authorize_instance(name=random_instance_name)

				assert  ai.name == random_instance_name

	def test_instance_functionality(self):
			app = c.authenticate_application(app_url=app_url, 
                                          api_token=api_token, 
                                          instance_id=instance_id)
			assert len(app.users) > 0

			for u in app.users.itervalues():
				for w in u.wallets.itervalues():
					assert w.balance >= 0

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

			dev = c.authenticate_developer(email=dev_email, privkey=privkey, override = True)
			assert app.name == dev.applications['default'].name


			

