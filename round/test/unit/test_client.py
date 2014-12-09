# client_test.py
#
# Copyright 2014 BitVault, Inc. dba Gem

from pytest import mark, raises

import patchboard
import round
from round.client import Client as RoundClient

from helpers import *
from fixtures import *

mark.usefixtures(client, developers, developer, alt_developer,
                 apps, app, alt_app, users, user, alt_user,
                 wallets, wallet, accounts, account, addresses, address)

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
        assert client.context.schemes[u'Gem-Developer']['credential'] == cred.format(
            developer.email)
        assert client.context.privkey == privkey()

        with raises(ValueError):
            d = client.authenticate_developer(developer.email, privkey=privkey())


    def test_authenticate_application(self, client, app):
        with raises(round.AuthenticationError):
            apps = app.users.list()

        client.authenticate_application(app.url, app.api_token,
                                        instance_id(), fetch=False)

        cred = 'instance_id="{}", api_token="{}"'
        assert client.context.schemes[u'Gem-Application']['credential'] == cred.format(
            instance_id(),
            app.api_token)

        assert client.context.app_url == app.url
        assert client.context.api_token == app.api_token
        assert client.context.instance_id == instance_id()

        with raises(ValueError):
            client.authenticate_application(app.url, app.api_token,
                                            instance_id(), fetch=False)


    # def test_developers(self, developers):
    #     assert developers
    #     assert type(developers) == round.developers.Developers

    # def test_developer(self, developer):
    #     assert developer
    #     assert type(developer) == round.developers.Developer

    # def test_developer_update(self, developer):
    #     new_email = email()
    #     developer = developer.update(email=new_email)
    #     assert developer
    #     assert type(developer) == round.developers.Developer
    #     assert developer.email == new_email

    # def test_apps(self, apps):
    #     assert type(apps) == round.dict_wrappers.Applications

    # def test_app(self, app):
    #     assert app
    #     assert type(app) == round.wrappers.Application

    # def test_app_update(self, app):
    #     app = app.update(name="wrenches")
    #     assert app
    #     assert type(app) == round.wrappers.Application
    #     assert app.name == "wrenches"

    # def test_users(self, users):
    #     assert type(users) == round.dict_wrappers.Users

    # def test_user(self, user):
    #     assert(user)
    #     assert type(user) == round.wrappers.User

    # def test_user_update(self, user):
    #     new_name = {"first_name": "John", "last_name": "Johnson"}
    #     user = user.update(**new_name)
    #     assert user
    #     assert type(user) == round.wrappers.User
    #     for (key, value) in new_name.items():
    #         assert user[key] == value

    # def test_wallets(self, wallets):
    #     assert type(wallets) == round.dict_wrappers.Wallets

    # def test_wallet(self, wallet):
    #     assert wallet
    #     assert wallet.is_unlocked()
    #     assert type(wallet) == round.wrappers.Wallet

    # def test_wallet_update(self, wallet):
    #     wallet = wallet.update(name="support")
    #     assert wallet
    #     assert type(wallet) == round.wrappers.Wallet
    #     assert wallet.name == "support"

    # def test_accounts(self, accounts):
    #     assert type(accounts) == round.dict_wrappers.Accounts

    # def test_account(self, account):
    #     assert account
    #     assert type(account) == round.wrappers.Account

    # def test_account_update(self, account):
    #     account = account.update(name="staples")
    #     assert account
    #     assert type(account) == round.wrappers.Account
    #     assert account.name == "staples"


    # def test_addresses(self, addresses):
    #     assert addresses is not None
    #     assert type(addresses) == round.list_wrappers.Addresses

    # def test_address(self, address):
    #     assert address is not None
    #     assert type(address) == patchboard.util.SchemaStruct

    # def test_basic_auth(self, developer, app):
    #     auth = dict(email=developer.email, password=password())
    #     client = round.authenticate(developer=auth)
    #     developer = client.developer
    #     assert developer
    #     for name, application in developer.applications.iteritems():
    #         assert application
    #         assert type(app) == round.wrappers.Application
