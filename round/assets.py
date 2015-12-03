# -*- coding: utf-8 -*-
# assets.py
#
# Copyright 2014-2015 BitVault, Inc. dba Gem

from __future__ import unicode_literals

import logging
from .config import *
from .errors import *
from patchboard.response import ResponseError

from coinop.transaction import Transaction as CoinopTx

from .wrappers import *
from .subscriptions import Subscriptions
from .addresses import Addresses
from .netki import NetkiNames
from .transactions import Transaction, Transactions

logger = logging.getLogger(__name__)

class Assets(DictWrapper):
    """A collection of round.Asset objects.

    Args:
      resource: Asset patchboard.Resource object
      client: authenticated round.Client object
      wallet: round.Wallet object to which this Asset belongs.

    Returns:
      The new round.Accounts object.
    """

    def __init__(self, resource, client, wallet=None, populate=False):
        self.wallet = wallet
        super(Assets, self).__init__(resource, client, populate)


    # TODO true docstrings
    def create(self, name, description='',
               network='bcy', protocol='openassets',
               issuing_seed=None, fungible=False):
        """Create a new Asset object and add it to this Assets collection.

        Args:
          name (str): Human-readable name for the asset
          description (str, optional): Information about the nature and purpose
            of this Asset.
          network (str): Blockchain underlying the asset definition.
            Can be one of: [ bitcoin, bitcoin_testnet,
                             litecoin, dogecoin,
                             bcy ]
          protocol (str): System for representing assets via raw transactions
            Can be one of: [ openassets ]
          issuing_seed (str, optional): private secp256k1 key that will be
            required to issue new coins/units of unlocked assets.

        Returns: The new round.Asset
        """
        # if not network in SUPPORTED_NETWORKS:
        #     raise ValueError('Network not valid!')

        asset = self.wrap(
            self.resource.create(
                dict(name         = name,
                     network      = network,
                     description  = description,
                     protocol     = protocol,
                     issuing_seed = issuing_seed,
                     fungible     = fungible)))

        return self.add(asset)

    def wrap(self, resource):
        return Asset(resource, self.client, self.wallet)


class Asset(Wrapper, Updatable):
    """Assets are second-order objects that can be represented on a blockchain.

    Gem abstracts away the protocol-level details and allows you to interact with
    assets that use different protocols (e.g. OpenAssets, Elements, ColoredCoins)
    using the same interface.

    Since protocols use slightly different terminology, it is worth clarifying
    that a Gem Asset is a representation of an asset _type_, not an individual
    instance of one.

    An example of an asset could be "Gem stock," NOT "one share of Gem stock."

    Fungibility:
      Assets can either be fungible or non-fungible.
      Fungible assets behave like currencies where value can be divided using
      convention change outputs to the granularity of the currency's atomic units
      which are indistinguishable from each other (e.g. satoshis in bitcoin)

      By contrast, units non-fungible assets are not divisble. When you issue
      non-fungible assets, you create a number of discrete, distinct Asset Units.
      It follows that you would use non-fungible assets to represent non-fungible
      entities, e.g. house deeds.

    Attributes:
      units (round.AssetUnits): Collection of AssetUnits of this Asset type.

    Args:
      resource (patchboard.Resource): server-side Asset object
      client (round.Client)
      wallet (round.Wallet)
    """

    def __init__(self, resource, client, wallet):
        super(Asset, self).__init__(resource, client)
        self.wallet = wallet

    def is_locked(self):
        """An Asset is locked if no more units of its type may be issued."""
        return self.locked

    def update(self, **kwargs):
        """Update the Asset resource with specified content.

        Args:
          name (str): Human-readable name for the asset
          description (str): Information about the nature and purpose of this
            Asset.
          locked (boolean): Setting the locked flag will prevent new units from
            being issued/minted. This does NOT prove that no new units of type
            asset can be created, only that Gem will reject any requests to do so

        Returns: the updated Asset object.
        """
        return self.__class__(self.resource.update(kwargs),
                              self.client)

    def issue(self, **kwargs):
        """Short description

        MORE DESCRIPTION

        Args:
          outputs (better name needed)
          whatever (str, optional): TODO

        Returns:
          Something or other
        """

        # Check that wallet is unlocked
        if self.wallet.is_locked():
            raise DecryptionError("This wallet must be unlocked with "
                                  "wallet.unlock(passphrase)")

        # First create the unsigned tx.
        content = dict(outputs=kwargs['payees'],
                       #todo accept fee_source
                       fee_source=self.wallet.attributes['key'])

        tx = self.resource.issue(content)
        return Transaction(tx, self.client)

    def balances_at(self, utxo_confirmations=6):
        """Return the confirmed, claimed (reserved for a pending, unsigned
        transaction), and available balances, where the threshold for
        confirmed is the value of `utxo_confirmations`.

        Args:
          utxo_confirmations (int): the # of confirmations to use when computing
            balances.

        Returns:
          A dict of form { u'available_balance': 0,
                           u'claimed_balance': 0,
                           u'confirmed_balance': 0,
                           u'utxo_confirmations': 0 }
        """
        return self.resource.available(
            {'utxo_confirmations': utxo_confirmations}).__dict__['data']

    def transactions(self, **query):
        """Fetch and return Transactions involving any Address inside this
        Account.
        Note that this call is not cached. If you want to store a copy, you
        must assign it to a local variable, and call .refresh() when you need
        updated data

        Args:
          status (str or list, optional): One or a list of
            ["unsigned", "unapproved",
             "confirmed", "unconfirmed",
             "canceled", "denied"]
          type (str, optional): One of ["incoming", "outgoing"]

        Returns:
          A collection of matching Transactions
        """
        if 'status' in query and isinstance(query['status'], list):
            query['status'] = ','.join(map(str, query['status']))

        transaction_resource = self.resource.transactions(query)
        return Transactions(transaction_resource, self.client, populate=True)

    @property
    @cacheable
    def subscriptions(self):
        """Return the cached Subscriptions object for this Account."""
        return self.get_subscriptions()

    def get_subscriptions(self, fetch=False):
        """Return this Account's subscriptions object, populating it if fetch is True."""
        return Subscriptions(
            self.resource.subscriptions, self.client, populate=fetch)

    @property
    @cacheable
    def addresses(self):
        """Fetch and return an updted list of Addresses inside this Account."""
        return self.get_addresses()

    def get_addresses(self, fetch=False):
        """Return the Account's addresses object, populating it if fetch is True."""
        return Addresses(self.resource.addresses, self.client, populate=fetch)

    @property
    @cacheable
    def netki_names(self):
        """Fetch and return an updated list of NetkiNames inside this Account."""
        return self.get_netki_names()

    def get_netki_names(self, fetch=False):
        """Return the Account's NetkiNames object, populating it if fetch is True."""
        return NetkiNames(self.resource.netki_names, self.client, populate=fetch)
