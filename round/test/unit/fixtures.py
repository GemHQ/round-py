# unit/fixtures.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import pytest


import round

# This is the one time this is OK--we use everything in the module
from helpers import (round_url, email, password, app_name, callback_url,
                     locked_wallet_name, locked_wallet_passphrase,
                     wallet_name, wallet_passphrase, account_name)


@pytest.fixture(scope=u'function')
def initial_client():
    return round.client(round_url())


@pytest.fixture(scope=u'function')
def developers(initial_client):
    return initial_client.developers


@pytest.fixture(scope=u'function')
def developer(developers):
    return developers.create(email=email(), password=password())


@pytest.fixture(scope=u'function')
def apps(developer):
    return developer.applications


@pytest.fixture(scope=u'function')
def app(apps):
    return apps.create(name=app_name(), callback_url=callback_url())


@pytest.fixture(scope=u'function')
def user(app):
    return app.users.create(first_name="James", last_name="Jameson")


@pytest.fixture(scope=u'function')
def users(app):
    return app.users


@pytest.fixture(scope=u'function')
def wallets(user):
    return user.wallets


@pytest.fixture(scope=u'function')
def wallet(user):
    backup_seed, new_wallet = user.wallets.create(
        name=wallet_name(),
        passphrase=wallet_passphrase())
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
