# -*- coding: utf-8 -*-
# functional/test_account.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
from round.users import User
from round.wallets import *
from round.accounts import *
from round.transactions import *
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
admin_token = admin_token()
app_url = app_url()
dev_email= dev_email()
random_instance_name = random_instance_name()

create = test_create_methods()

c = round.client()
u = c.authenticate_device(api_token=api_token,
                          user_token=user_token,
                          device_id=device_id,
                          user_url=user_url,
                          override=True)

w = u.wallets['default']

account_attribute_keys = [u'addresses', u'name', u'transactions', u'i', u'url', u'payments', u'key', u'path', u'balance', u'pending_balance']

class TestAccount:
    def test_account_collection(self):
        assert isinstance(w.accounts, Accounts)

        for n, a in w.accounts.iteritems():
            assert isinstance(n, basestring)
            assert isinstance(a, Account)

        assert len(w.accounts) > 0

    def test_account_creation(self):
        old_accounts_length = len(w.accounts)
        if create:
            new_account = w.accounts.create(name=random_account_name())
            assert isinstance(new_account, Account)
            assert len(new_account.attributes) == 10
            assert account_attribute_keys == new_account.attributes.keys()
            assert new_account.balance == 0
            assert new_account.pending_balance == 0

    def test_account_update(self):
        a = w.accounts['default']
        with raises(round.AuthenticationError):
            a.update(name='new name')

    def test_account_pay(self):
        a = w.accounts['newChecking']
        previous_balance = a.balance
        if create:
            payee =[{'address':w.accounts['default'].addresses.create().string, 'amount':20000}]
            payment = a.pay(payee)
            assert isinstance(payment.data, dict)
            assert payment.status == 'unconfirmed'
            assert len(payment.hash) == 64

            refreshed_account = a.refresh()
            assert refreshed_account.pending_balance == -payee[0]['amount'] + -payment.fee

    def test_address_creation(self):
        a = w.accounts['addressCreations']
        prev_address_size = len(a.addresses)

        address = a.addresses.create()

        assert isinstance(address, patchboard.util.SchemaStruct)
        assert address.path
        assert address.string
        assert address.string[0] == '2'
        assert len(a.addresses) == prev_address_size + 1

    def test_receive_payment(self):
        if create:
            a = w.accounts['newChecking']
            old_balance = a.balance
            old_incoming_tx = len(a.transactions(type='incoming'))

            address = a.addresses.create().string
            getMoney(address)

            time.sleep(120)

            assert old_balance < a.refresh().balance
            assert old_incoming_tx < len(a.refresh().transactions(type='incoming'))

    def test_transaction_collection(self):
        a = w.accounts['newChecking']
        txs = a.transactions()
        tx = txs[0]
        assert isinstance(txs, Transactions)
        assert isinstance(tx, Transaction)

        tx_data = tx.resource.to_hash()
        data_keys = [u'status', u'inputs',
                    u'lock_time', u'fee',
                    u'hash', u'version',
                    u'url', u'outputs',
                    u'created_at', u'value',
                    u'confirmations', 
                    u'key', u'type']

        assert tx_data.keys() == data_keys
        

        for t in a.transactions(type='incoming'):
            assert t.type == 'incoming'

        for t in a.transactions(type='outgoing'):
            assert t.type == 'outgoing'
