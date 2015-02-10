# test_account.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
from round.users import User
from round.wallets import *
from round.accounts import *
from coinop.bit.multiwallet import *

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
u = c.authenticate_device(api_token=api_token,
                           user_token=user_token,
                           device_id=device_id,
                           user_url=user_url,
                           override=True)

w = u.wallets['default']


class TestAccount:
	def test_account_collection(self):
		assert True

	def test_account_management(self):
		assert True

	def test_account_details(self):
		assert True