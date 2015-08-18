#! /usr/bin/env python
#
# Hey guys, here's a quick demo of how to use Gem's python client library to
# build something awesome and quick. Below I've outlined the specs for a simple
# CLI wallet app.
#
# round-cli: A super simple command-line bitcoin wallet to show off Gem's API!
#
# Requirements:
# - A user can create a new Gem multisig wallet
# - A user can log into an existing Gem multisig wallet.
# - A user can view/create accounts within their wallet.
# - A user can get an address to receive money.
# - A user can send money to any address.
# - Support for bitcoin, testnet, litecoin, and dogecoin.
#
# First! We need to install the round package through pip.
# And after that, we'll need a developer account. That'll take a second, so
# let's grab the API Token from the dev console (sandbox.gem.co)
#

from __future__ import unicode_literals
from future.utils import iteritems

from json import dumps, loads
from pprint import pprint as pp
from os.path import expanduser
from sys import argv
from shutil import move
from tabulate import tabulate

# Every CLI needs argument parsing
from argparse import ArgumentParser

#secure password entry
from getpass import getpass

#for providing MFA tokens in a browser
from webbrowser import open_new

from round import client as roundclient # woo!

def print_wallets():
    global wallets

    headers = ['#', 'Wallet']
    table = []
    count = 1
    for name, wallet in iteritems(wallets):
        table.append([ count, name ])
        count += 1
    print("\n" + tabulate(table, headers=headers))

def print_wallet(wallet, fetch=True):
    headers = ['#', 'Account', 'Network', 'Confirmed', 'Pending', 'Available']
    try:
        table = []
        count = 1
        for name, account in iteritems(wallet.accounts):
            if fetch:
                account = account.refresh()
            table.append([ count, name, account.network,
                           account.balance,
                           account.pending_balance,
                           account.available_balance ])
            count += 1
        print("\n" + tabulate(table, headers=headers))
    except Exception as e:
        print(e)

def select_wallet():
    global thewallet
    print_wallets()
    try:
        wallet_number = raw_input("\nEnter wallet number: ")
        print_wallet(wallets.values()[int(wallet_number) - 1], fetch=False)
        return wallets.values()[int(wallet_number) - 1]
    except:
        print("Invalid selection: {}\n".format(wallet_number))
        return thewallet if thewallet else select_wallet()

def select_account(wallet):
    print_wallet(wallet, fetch=False)
    acct_number = raw_input("\nEnter account number: ")
    return wallet.accounts.values()[int(acct_number) - 1]

NETWORKS = ['bitcoin', 'bitcoin_testnet', 'litecoin', 'dogecoin']
def select_network():
    prompt = "What kind of account?"
    for i,v in enumerate(NETWORKS):
        prompt = ("{}\n"
                  "{}. {}").format(prompt, i + 1, v)

    acct_number = raw_input("{}\n"
                            "> ".format(prompt))

    return NETWORKS[int(acct_number) - 1]

def pop_a_browser(uri):
    open_new(uri)
    raw_input("Provide your MFA in the browser window to confirm this action. "
              "Press enter when you're done ... ")

def process_command():
    global thewallet

    command = raw_input("""
Choose an action:
0. Select wallet
1. Send coin
2. Receive coin (generate a new address)
3. List transactions
4. Cancel unapproved transactions
5. Create new account
> """)

    try:
        command = int(command)
    except:
        print("\n[ Unknown command ]")
        print_wallet(thewallet)
        return None

    if command > 0 and command < 6:
        theaccount = select_account(thewallet)

    if command == 0:
        thewallet = select_wallet()

    elif command == 1:
        if thewallet.is_locked():
            # unlocking a user wallet decrypts the primary private key
            # used to make signatures.
            passphrase = getpass()
            thewallet.unlock(passphrase)

        if thewallet.application and not hasattr(thewallet.application, 'totp'):
            thewallet.application.set_totp(
                getpass(prompt="Enter your application's totp secret: "))


        dest_address = raw_input("\nDestination address: ")
        amount = raw_input("\nTransaction amount (satoshis): ")
        tx = theaccount.pay(
            payees=[dict(address=dest_address, amount=int(amount))],
            utxo_confirmations=1)

        if thewallet.application:
            tx.approve(thewallet.application.get_mfa)
            print("\nTransaction approved!")
        else:
            pop_a_browser(tx.mfa_uri)

    elif command == 2:
        # Generating an address is eeeeeasy
        print("Pay into this address: {}".format(
            theaccount.addresses.create()['string']))
        raw_input("Press enter to continue or CTRL-C to quit")

    elif command == 3:
        for tx in theaccount.transactions():
            pp(tx.attributes)

    elif command == 4:
        for tx in theaccount.transactions(type='outgoing',
                                       status=['unsigned', 'unapproved']):
            tx.cancel()

    elif command == 5:
        network = select_network()
        name = raw_input("Account name> ")
        thewallet.accounts.create(name=name, network=network)
        print_wallet(thewallet)
    else:
        # wat?
        print("\n[ Unknown command ]")
        print_wallet(thewallet)
    print


if __name__ == '__main__':
    config_filename = expanduser('~/.gemwallet')

    parser = ArgumentParser(
        description="A simple Gem-back command-line bitcoin wallet.",
        fromfile_prefix_chars='@')
    parser.add_argument('-a', '--api_token',
                        help="Your api_token")
    parser.add_argument('-m', '--admin_token',
                        help="Your admin_token (for application wallets)")
    parser.add_argument('-u', '--url',
                        help="Gem API URL (https://api.gem.co)",
                        default="https://api.gem.co")
    parser.add_argument('-d', '--device_token',
                        help="Your device_token",
                        default=None)
    parser.add_argument('-b', '--backup_seed',
                        help="Your backup seed",
                        default=None)
    parser.add_argument('-e', '--email',
                        help="Gem user email address",
                        default=None)

    args = parser.parse_args(['@{}'.format(config_filename)] + argv[1:])
    api_token = args.api_token
    device_token = args.device_token
    admin_token = args.admin_token
    backup_seed = args.backup_seed
    url = args.url
    email = args.email

    # Now we need a client to talk to Gem.
    client = roundclient(url=url)

    # Now we have to authenticate. If the admin_token is provided, we'll authenticate
    # as an application.
    app = None
    if admin_token and admin_token != 'None':
        app = client.authenticate_application(api_token, admin_token)

    # If we don't have application creds, then maybe we're running as a user!
    user = None
    if device_token and device_token != 'None' and email and (not app):
        user = client.authenticate_device(api_token, device_token, email=email)



    # If we don't have the credentials we need to authenticate yet, we can get them!
    if (not device_token) and email and (not admin_token):
        # First we authenticate with just our api_token for identification
        client.authenticate_identify(api_token)

        try:
            # Let's try to get an existing user first. It'll throw an exception
            # if the account doesn't exist.
            user = client.user(email)

            # Since we don't have a device_token from them, we'll need to create
            # A new user device to associate our app with their account.
            device_token, mfa_uri = user.devices.create(name="Gem CLI")

            # Then they can visit the mfa_uri we receive back to authorize with
            # their 2FA authorization code (via SMS).
            pop_a_browser(mfa_uri)
        except:
            # Whoops, looks like the user with `email` doesn't have an account!
            # Let's make them one.
            print("Pick a secure passphrase for your Gem account: ")
            passphrase = getpass()
            device_token = client.users.create(email=email,
                                               passphrase=passphrase,
                                               device_name="Gem CLI")
            backup_seed  = raw_input("Check your email to confirm your new wallet, "
                                     "then enter your backup seed (or press enter): ")

        print("device_token: {}".format(device_token))


        # Cool, so now when execution continues, we'll have a device_token authorized on
        # our app, so we can authenticate as the user!

        # We're gonna want to save those creds,
        # * particularly the device_token and backup_seed *

        yn = raw_input("\nSave your credentials to ~/.gemwallet? [y/N]: ")
        if yn.lower() == 'y':
            move(config_filename, "{}.bak".format(config_filename))
            fh = open(config_filename, 'w')
            fh.write(("-a{}\n"
                      "-m{}\n"
                      "-u{}\n"
                      "-d{}\n"
                      "-e{}\n"
                      "-b{}").format(
                          api_token, admin_token, url, device_token, email, backup_seed))
            fh.close()

            if (not user) and device_token:
                user = client.authenticate_device(
                    api_token=api_token, device_token=device_token, email=email)

    thewallet = None

    if app:
        wallets = app.wallets
        thewallet = select_wallet()
    if user:
        wallets = {user.email: user.wallet}
        thewallet = user.wallet


    # off to the races! we hope...
    while True:
        try:
            process_command()
        except Exception as e:
            print("\n[ Problem: {} ]".format(e))
