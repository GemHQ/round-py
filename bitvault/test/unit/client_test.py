# client_test.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

import patchboard
import bitvault

from helpers import email

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
        # hides the bitvault.client module
        #assert isinstance(initial_client, bitvault.client.Client)

    def test_users(self, users):
        assert users
        assert type(users) == bitvault.wrappers.Users

    def test_user(self, user):
        assert user
        assert type(user) == bitvault.wrappers.User

    def test_user_update(self, user):
        new_email = email()
        user = user.update(email=new_email)
        assert user
        assert type(user) == bitvault.wrappers.User
        assert user.email == new_email

    def test_apps(self, apps):
        assert type(apps) == bitvault.dict_wrappers.Applications

    def test_app(self, app):
        assert app
        assert type(app) == bitvault.wrappers.Application

    def test_wallets(self, wallets):
        assert type(wallets) == bitvault.dict_wrappers.Wallets

    def test_locked_wallet(self, locked_wallet):
        assert locked_wallet
        assert locked_wallet.is_locked()
        assert type(locked_wallet) == bitvault.wrappers.Wallet

    def test_wallet(self, wallet):
        assert wallet
        assert wallet.is_unlocked()
        assert type(wallet) == bitvault.wrappers.Wallet

    def test_accounts(self, accounts):
        assert type(accounts) == bitvault.dict_wrappers.Accounts

    def test_account(self, account):
        assert account
        assert type(account) == bitvault.wrappers.Account

    def test_addresses(self, addresses):
        assert addresses is not None
        assert type(addresses) == bitvault.list_wrappers.Addresses

    def test_address(self, address):
        assert address is not None
        assert type(address) == patchboard.util.SchemaStruct
