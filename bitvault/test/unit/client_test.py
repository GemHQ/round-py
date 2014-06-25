# client_test.py
#
# Copyright 2014 BitVault.


from __future__ import print_function

import pytest

from fixtures import (initial_client, users, user, app, locked_wallet,
                      wallet)
pytest.mark.usefixtures(initial_client, users, user, app, locked_wallet,
                        wallet)


def test_initial_client_creation(initial_client):
    assert initial_client


def test_users_creation(users):
    assert users


def test_user_creation(user):
    assert user


def test_app_creation(app):
    assert app


def test_locked_wallet_creation(locked_wallet):
    assert locked_wallet
    assert locked_wallet.is_locked()


def test_wallet_creation(wallet):
    assert wallet
    assert wallet.is_unlocked()
