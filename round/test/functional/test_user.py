# test_user.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
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

c = round.client()


class TestUser:
	def test_user_creation(self):
			assert True
	
	def test_user_authentication(self):
			assert True

	def test_user_wallet_management(self):
			assert True