# -*- coding: utf-8 -*-
# functional/test_developer.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises
from helpers import *
from round.applicationspy import *

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

    def test_application_reset(self):
        dev = c.authenticate_developer(email=dev_email, privkey=privkey, override=True)
        app = dev.applications['testReset']
        old_api_token = app.api_token

        reset_app = app.reset()
        new_api_token = reset_app.api_token
        assert isinstance(reset_app, Application)
        assert new_api_token != old_api_token
        assert app.attributes['key'] == reset_app.attributes['key']

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
        assert isinstance(w.primary_private_seed, type(None))
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
