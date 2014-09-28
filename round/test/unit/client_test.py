# client_test.py
#
# Copyright 2014 BitVault, Inc. dba Gem


from __future__ import print_function

import pytest

import patchboard
import round

from helpers import email, password

from fixtures import (initial_client, users, user, app, apps, wallets,
                      locked_wallet, wallet, accounts, account, addresses,
                      address)
pytest.mark.usefixtures(initial_client, users, user, app, apps, wallets,
                        locked_wallet, wallet, accounts, account, addresses,
                        address)


class TestResourceCreation:

    def test_initial_client(self, initial_client):
        assert initial_client
        # This currently fails because the client() function in __init__.py
        # hides the round.client module
        #assert isinstance(initial_client, round.client.Client)

    def test_users(self, users):
        assert users
        assert type(users) == round.wrappers.Users

    def test_user(self, user):
        assert user
        assert type(user) == round.wrappers.User

    def test_user_update(self, user):
        new_email = email()
        user = user.update(email=new_email)
        assert user
        assert type(user) == round.wrappers.User
        assert user.email == new_email

    def test_apps(self, apps):
        assert type(apps) == round.dict_wrappers.Applications

    def test_app(self, app):
        assert app
        assert type(app) == round.wrappers.Application

    def test_app_update(self, app):
        app = app.update(name="wrenches")
        assert app
        assert type(app) == round.wrappers.Application
        assert app.name == "wrenches"

    def test_wallets(self, wallets):
        assert type(wallets) == round.dict_wrappers.Wallets

    def test_locked_wallet(self, locked_wallet):
        assert locked_wallet
        assert locked_wallet.is_locked()
        assert type(locked_wallet) == round.wrappers.Wallet

    def test_wallet(self, wallet):
        assert wallet
        assert wallet.is_unlocked()
        assert type(wallet) == round.wrappers.Wallet

    #def test_wallet_update(self, wallet):
        #wallet = wallet.update(name="support")
        #assert wallet
        #assert type(wallet) == round.wrappers.Wallet
        #assert wallet.name == "support"


    def test_accounts(self, accounts):
        assert type(accounts) == round.dict_wrappers.Accounts

    def test_account(self, account):
        assert account
        assert type(account) == round.wrappers.Account

    def test_account_update(self, account):
        account = account.update(name="staples")
        assert account
        assert type(account) == round.wrappers.Account
        assert account.name == "staples"


    def test_addresses(self, addresses):
        assert addresses is not None
        assert type(addresses) == round.list_wrappers.Addresses

    def test_address(self, address):
        assert address is not None
        assert type(address) == patchboard.util.SchemaStruct

    def test_basic_auth(self, user, app):
        auth = dict(email=user.email, password=password())
        client = round.authenticate(developer=auth)
        user = client.user
        assert user
        for name, application in user.applications.iteritems():
            assert application
            assert type(app) == round.wrappers.Application

