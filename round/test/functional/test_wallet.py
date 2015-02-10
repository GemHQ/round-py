# test_wallet.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
from round.users import User
from round.wallets import *
from round.accounts import *
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

class TestWallet:
	def test_wallet_collection(self):
		assert isinstance(u.wallets, Wallets)
		assert len(u.wallets) > 0

		for n in u.wallets.iterkeys():
			w = u.wallets[n]
			assert isinstance(w, Wallet)
			assert n == w.name

	def test_create_wallet(self):
		if create:
			old_num_wallets = len(u.wallets)
			backup_seed, w = u.wallets.create(name=random_wallet_name(),passphrase='password')
			assert isinstance(backup_seed, basestring)
			assert len(backup_seed) == 111
			assert backup_seed[0:4] == 'tprv'
			assert isinstance(w, Wallet)

			assert new_num_wallets == len(u.refresh().wallets)

	def test_wallet_functionality(self):
		w = u.wallets['default']
		assert isinstance(w.balance, int)
		assert len(w.attributes) == 13
		assert w.name == 'default'
		assert not w.primary_private_seed is None 
		assert w.is_locked()

		w.unlock('password')
		assert w.is_unlocked()
		assert not w.is_locked()

		balance = w.balance
		assert isinstance(balance, int)


	
	def test_account_management(self):
			assert True

	def test_account_details(self):
			assert True