# unit/fixtures.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import pytest


import round

from helpers import *


@pytest.fixture(scope=u'function')
def client():
    return round.client(round_url())


@pytest.fixture(scope=u'function')
def developers(client):
    return client.developers


@pytest.fixture(scope=u'function')
def developer(developers):
    return developers.create(email=email(), pubkey=pubkey())


@pytest.fixture(scope=u'function')
def alt_developer(developers):
    return developers.create(email="alt{}".format(email()), pubkey=pubkey())


@pytest.fixture(scope=u'function')
def apps(developer):
    developer.client.authenticate_developer(email=developer.email, privkey=privkey())
    return developer.applications


@pytest.fixture(scope=u'function')
def app(apps):
    return apps.create(name=app_name())


@pytest.fixture(scope=u'function')
def instance_id():
    return "bogus-instance-id"

@pytest.fixture(scope=u'function')
def alt_app(apps):
    return apps.create(name="alt{}".format(app_name()))


@pytest.fixture(scope=u'function')
def user(app):
    return app.users.create(email=email(), passphrase=passphrase(),
                            first_name="James", last_name="Jameson")


@pytest.fixture(scope=u'function')
def alt_user(app):
    return app.users.create(email="alt{}".format(email()),
                            passphrase=passphrase(),
                            first_name="Jane", last_name="Jameson")


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
        passphrase=passphrase())
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
