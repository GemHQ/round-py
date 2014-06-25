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
