# unit/helpers.py
#
# Copyright 2014 BitVault, Inc. dba Gem
#
# Broken out of fixtures.py so that in the future they can be used in the
# tests as well.

import pytest
import time
from random import randint


def round_url():
    return u"https://api-develop.gem.co"
    #return u"http://api.gem.co"


def current_milli_time():
    return int(round(time.time()))


def email():
    return u'{0}@gem.co'.format(randint(0, 2**32 - 1))


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


def account_name():
    return u'office supplies'
