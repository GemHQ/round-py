# unit/fixtures.py
#
# Copyright 2014 BitVault.


import pytest


import bitvault

# This is the one time this is OK--we use everything in the module
from helpers import (bitvault_url, email, password, app_name, callback_url,
                     locked_wallet_name, locked_wallet_passphrase,
                     wallet_name, wallet_passphrase, account_name)


@pytest.fixture(scope=u'function')
def initial_client():
    return bitvault.client(bitvault_url())


@pytest.fixture(scope=u'function')
def users(initial_client):
    return initial_client.users


@pytest.fixture(scope=u'function')
def user(users):
    return users.create(email=email(), password=password())


@pytest.fixture(scope=u'function')
def apps(user):
    return user.applications


@pytest.fixture(scope=u'function')
def app(apps):
    return apps.create(name=app_name(), callback_url=callback_url())


@pytest.fixture(scope=u'function')
def wallets(app):
    return app.wallets


@pytest.fixture(scope=u'function')
def locked_wallet(wallets):
    backup_seed, wallet = wallets.create(
        name=locked_wallet_name(),
        passphrase=locked_wallet_passphrase())
    return wallet


@pytest.fixture(scope=u'function')
def wallet(app):
    backup_seed, new_wallet = app.wallets.create(
        name=wallet_name(),
        passphrase=wallet_passphrase())
    new_wallet.unlock(wallet_passphrase())
    return new_wallet


@pytest.fixture(scope=u'function')
def accounts(wallet):
    return wallet.accounts


@pytest.fixture(scope=u'function')
def account(accounts):
    return accounts.create(name=account_name())


@pytest.fixture(scope=u'function')
def addresses(account):
    return account.addresses


@pytest.fixture(scope=u'function')
def address(addresses):
    return addresses.create()
