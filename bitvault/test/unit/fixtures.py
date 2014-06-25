# unit/fixtures.py
#
# Copyright 2014 BitVault.


import time
import pytest


import bitvault


def bitvault_url():
    return u"http://localhost:8998"


def current_milli_time():
    return int(round(time.time()))


def email():
    return u'{0}@bitvault.io'.format(current_milli_time())


def password():
    return u'incredibly_secure'


def app_name():
    return u'bitcoins_r_us'


def locked_wallet_name():
    return u'my locked wallet'


def wallet_name():
    return u'my favorite wallet'


def locked_wallet_passphrase():
    return u"a very bad passphrase"


def wallet_passphrase():
    return u"wrong pony generator brad"


def callback_url():
    return u'https://someapp.com/callback'


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
def app(user):
    return user.applications.create(name=app_name(),
                                    callback_url=callback_url())


@pytest.fixture(scope=u'session')
def locked_wallet(app):
    return app.wallets.create(name=locked_wallet_name(),
                              passphrase=locked_wallet_passphrase())


@pytest.fixture(scope=u'session')
def wallet(app):
    new_wallet = app.wallets.create(name=wallet_name(),
                                    passphrase=wallet_passphrase())
    new_wallet.unlock(wallet_passphrase())
    return new_wallet
