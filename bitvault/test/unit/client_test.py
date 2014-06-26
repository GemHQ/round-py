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


def test_initial_client_creation(initial_client):
    assert initial_client
    # TODO: make this work. It currently fails because the client()
    # function in __init__.py hides the bitvault.client module
    #assert isinstance(initial_client, bitvault.client.Client)


def test_users_creation(users):
    assert users
    assert isinstance(users, bitvault.collections.Users)


def test_user_creation(user):
    assert user
    assert isinstance(user, bitvault.wrappers.User)


def test_apps_creation(apps):
    assert apps
    assert isinstance(apps, bitvault.collections.Applications)


def test_app_creation(app):
    assert app
    assert isinstance(app, bitvault.wrappers.Application)


def test_wallets_creation(wallets):
    assert wallets
    assert isinstance(wallets, bitvault.collections.Wallets)


def test_locked_wallet_creation(locked_wallet):
    assert locked_wallet
    assert locked_wallet.is_locked()
    assert isinstance(locked_wallet, bitvault.wrappers.Wallet)


def test_wallet_creation(wallet):
    assert wallet
    assert wallet.is_unlocked()
    assert isinstance(wallet, bitvault.wrappers.Wallet)


def test_accounts_creation(accounts):
    assert accounts
    assert isinstance(accounts, bitvault.collections.Accounts)


def test_account_creation(account):
    assert account
    assert isinstance(account, bitvault.wrappers.Account)


def test_addresses_creation(addresses):
    assert addresses
    assert isinstance(addresses, patchboard.resources.Addresses)


def test_address_creation(address):
    assert address
    assert isinstance(address, patchboard.util.SchemaStruct)
