# -*- coding: utf-8 -*-
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
def user(user_email, client):
    return client.users.create(email=user_email, passphrase=passphrase(),
                               first_name="James", last_name="Jameson")[1]


@pytest.fixture(scope=u'function')
def user_email():
    return email()


@pytest.fixture(scope=u'function')
def user_token():
    return "bogus-user-token"


@pytest.fixture(scope=u'function')
def device_id():
    return "bogus-device-id"


@pytest.fixture(scope=u'function')
def users(user, client):
    users = round.users.Users(None, client)
    users.add(user)


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
