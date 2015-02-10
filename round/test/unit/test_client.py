# -*- coding: utf-8 -*-
# client_test.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises

import patchboard
import round
from round.client import Client as RoundClient

from helpers import *
from fixtures import *

mark.usefixtures(client, developers, developer,
                 apps, app, users, user, wallets, wallet,
                 accounts, account, addresses, address)

class TestClient:

    def test_client_returns_a_Client(self, client):
        c1 = round.client(url=round_url())
        c2 = round.client(network=u'testnet')
        for c in [client, c1, c2]:
            assert type(c) == RoundClient

    def test_client_fails_with_bad_url(self):
        with raises(patchboard.exception.PatchboardError):
            round.client(url=u'bogus!')
        with raises(patchboard.exception.PatchboardError):
            round.client(url=u'http://www.google.com/')

    def test_client_fails_with_bad_network(self):
        with raises(round.UnknownNetworkError):
            round.client(network=u'bogus!')

    def test_client_has_properties(self, client, developers):
        pb = round._patchboard[round_url()]
        assert client.pb_client.main_pb is pb
        assert client.network == round.config.DEFAULT_NETWORK
        assert type(client.context) == round.Context
        assert client.resources is client.pb_client.resources
        assert type(client.resources) == patchboard.endpoints.Endpoints
        assert client.developers is developers
        assert type(client.developers) == round.developers.Developers
        assert type(client.users) == round.users.Users

    def test_authenticate_developer(self, client, developer):
        with raises(round.AuthenticationError):
            developer.get()

        d = client.authenticate_developer(developer.email, privkey=privkey())
        for field in d.attributes:
            assert d.attributes[field] == developer.attributes[field]

        cred = 'email="{}"'
        assert client.context.schemes[u'Gem-Developer'][u'credential'] == cred.format(
            developer.email)
        assert client.context.privkey == privkey()

        with raises(ValueError):
            d = client.authenticate_developer(developer.email, privkey=privkey())

    def test_authenticate_application(self, client, app, instance_id):
        with raises(round.AuthenticationError):
            apps = app.users.list()

        client.authenticate_application(app.url, app.api_token,
                                        instance_id, fetch=False)

        cred = 'instance_id="{}", api_token="{}"'
        assert client.context.schemes[u'Gem-Application'][u'credential'] == cred.format(
            instance_id,
            app.api_token)

        assert client.context.app_url == app.url
        assert client.context.api_token == app.api_token
        assert client.context.instance_id == instance_id

        with raises(ValueError):
            client.authenticate_application(app.url, app.api_token,
                                            instance_id, fetch=False)

    def test_authenticate_device(self, client, app, user, device_id, user_email,
                                 user_token):
        with raises(round.AuthenticationError):
            user = user.get()

        # With email
        client.authenticate_device(app.api_token, user_token, device_id,
                                   email=user_email, fetch=False)
        # With user_url
        client.authenticate_device(app.api_token, user_token, device_id,
                                   user_url=user.url, override=True, fetch=False)

        cred = 'user_token="{}", device_id="{}", api_token="{}"'
        assert client.context.schemes[u'Gem-Device'][u'credential'] == cred.format(
            user_token,
            device_id,
            app.api_token)

        assert client.context.user_token == user_token
        assert client.context.api_token == app.api_token
        assert client.context.user_email == user_email
        assert client.context.user_url == user.url
        assert client.context.device_id == device_id

        with raises(ValueError):
            client.authenticate_device(app.api_token, user_token, device_id,
                                       email=user_email, fetch=False)

        # fails without user_url or email
        with raises(ValueError):
            client.authenticate_device(app.api_token, user_token, device_id,
                                       override=True, fetch=False)

    def test_authenticate_otp(self, client, app, user):
        client.authenticate_otp(app.api_token, "key", "secret")

        cred = 'secret="{}", key="{}", api_token="{}"'
        assert client.context.schemes[u'Gem-OOB-OTP'][u'credential'] == cred.format(
            "secret",
            "key",
            app.api_token)

        assert client.context.key == "key"
        assert client.context.secret == "secret"
        assert client.context.api_token == app.api_token

        with raises(ValueError):
            client.authenticate_device(app.api_token, "key", "secret")

    def test_developer(self, client, developer):
        with raises(round.AuthenticationError):
            client.developer

        client.authenticate_developer(email=developer.email, privkey=privkey())
        assert client.developer.email == developer.email
