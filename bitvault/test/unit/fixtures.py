# unit/fixtures.py
#
# Copyright 2014 BitVault.


import pytest


import bitvault

# This is the one time this is OK--we use everything in the module
from helpers import (bitvault_url, email, password, app_name, callback_url,
                     locked_wallet_name, locked_wallet_passphrase,
                     wallet_name, wallet_passphrase, account_name)


@pytest.fixture(scope=u'session')
def initial_client():
    return bitvault.client(bitvault_url())


@pytest.fixture(scope=u'session')
def users(initial_client):
    return initial_client.users


@pytest.fixture(scope=u'session')
def user(users):
    return users.create(email=email(), password=password())


@pytest.fixture(scope=u'session')
def apps(user):
    return user.applications


@pytest.fixture(scope=u'session')
def app(apps):
    return apps.create(name=app_name(), callback_url=callback_url())


@pytest.fixture(scope=u'session')
def wallets(app):
    return app.wallets


@pytest.fixture(scope=u'session')
def locked_wallet(wallets):
    return wallets.create(name=locked_wallet_name(),
                          passphrase=locked_wallet_passphrase())


@pytest.fixture(scope=u'session')
def wallet(app):
    new_wallet = app.wallets.create(name=wallet_name(),
                                    passphrase=wallet_passphrase())
    new_wallet.unlock(wallet_passphrase())
    return new_wallet


@pytest.fixture(scope=u'session')
def accounts(wallet):
    return wallet.accounts


@pytest.fixture(scope=u'session')
def account(accounts):
    return accounts.create(name=account_name())


@pytest.fixture(scope=u'session')
def addresses(account):
    return account.addresses


@pytest.fixture(scope=u'session')
def address(addresses):
    return addresses.create()
