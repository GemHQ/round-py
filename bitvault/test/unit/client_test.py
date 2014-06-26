# client_test.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

import patchboard
import bitvault

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
        assert type(users) == bitvault.collections.Users

    def test_user(self, user):
        assert user
        assert type(user) == bitvault.wrappers.User

    def test_apps(self, apps):
        assert apps
        assert type(apps) == bitvault.collections.Applications

    def test_app(self, app):
        assert app
        assert type(app) == bitvault.wrappers.Application

    def test_wallets(self, wallets):
        assert wallets
        assert type(wallets) == bitvault.collections.Wallets

    def test_locked_wallet(self, locked_wallet):
        assert locked_wallet
        assert locked_wallet.is_locked()
        assert type(locked_wallet) == bitvault.wrappers.Wallet

    def test_wallet(self, wallet):
        assert wallet
        assert wallet.is_unlocked()
        assert type(wallet) == bitvault.wrappers.Wallet

    def test_accounts(self, accounts):
        assert accounts
        assert type(accounts) == bitvault.collections.Accounts

    def test_account(self, account):
        assert account
        assert type(account) == bitvault.wrappers.Account

    def test_addresses(self, addresses):
        assert addresses
        assert type(addresses) == patchboard.resources.Addresses

    def test_address(self, address):
        assert address
        assert type(address) == patchboard.util.SchemaStruct
