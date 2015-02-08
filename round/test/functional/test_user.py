# test_user.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
from round.users import User
from round.wallets import Wallet
from round.accounts import Account
import time
import patchboard
import round


pubkey = pubkey()
privkey = privkey()

api_token = api_token()
user_token = user_token()
device_id = device_id()
user_url = user_url()
email = email()
instance_id = instance_id()
app_url = app_url()
dev_email= dev_email()
random_instance_name = instance_name()

create = False

c = round.client(url=round_url(), network='testnet')

class TestUser:
	def test_user_creation(self):
			if create:
				backup_seed, user = client.users.create(email=email, passphrase='password')
				assert isinstance(backup_seed, basestring)
				assert isinstance(user, round.users.User)
	
	def test_user_authentication_email(self):
			u = c.authenticate_device(api_token=api_token,
                               user_token=user_token,
                               device_id=device_id,
                               email=email,
                               override=True)
			
			assert isinstance(u, User)
			assert len(u.attributes) == 7 
			assert u.user_token == user_token

	def test_user_authentication_user_url(self):
			u = c.authenticate_device(api_token=api_token,
                               user_token=user_token,
                               device_id=device_id,
                               user_url=user_url,
                               override=True)

			assert isinstance(u, User)
			assert len(u.attributes) == 7 
			assert u.user_token == user_token

	def test_user_wallet_management(self):
			assert True











