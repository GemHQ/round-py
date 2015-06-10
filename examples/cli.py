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

config_filename = expanduser('~/.gemwallet')

parser = ArgumentParser(
    description="A simple Gem-back command-line bitcoin wallet.",
    fromfile_prefix_chars='@')
parser.add_argument('-a', '--api_token', help="Your api_token")
parser.add_argument('-m', '--admin_token',
                    help="Your admin_token (for application wallets)")
parser.add_argument('-u', '--url',
                    help="Gem API URL (https://api.gem.co)",
                    default="https://api.gem.co")
parser.add_argument('-d', '--device_token',
                    help="Your device_token",
                    default=None)
parser.add_argument('-e', '--email', help="Gem user email address")

args = parser.parse_args(['@{}'.format(config_filename)] + argv[1:])
api_token = args.api_token
device_token = args.device_token
url = args.url
email = args.email

# Now we need a client to talk to Gem.
client = roundclient(url=url)

# Now we have to authenticate before sending requests:
client.authenticate_identify(api_token)
backup_seed = None


def pop_a_browser(uri):
    open_new(uri)
    raw_input("Provide your MFA in the browser window to confirm this action. "
              "Press enter when you're done ... ")

if not device_token:
    try:
        # Let's try to get an existing user first. It'll throw an exception
        # if the account doesn't exist.
        user = client.user(email) # wow, such difficult

        # Since we don't have a device_token from them, we'll need to create
        # A new user device to associate our app with their account.
        device_token, mfa_uri = user.devices.create(name="Gem CLI")

        # Then they can visit the mfa_uri we receive back to authorize with
        # their 2FA authorization code.
        pop_a_browser(mfa_uri)
    except:
        # Whoops, looks like they don't have an account! Let's make one.
        print("Pick a secure passphrase: ")
        passphrase = getpass()
        device_token = client.users.create(email=email,
                                           passphrase=passphrase,
                                           device_name="Gem CLI")
        backup_seed  = raw_input("Check your email to confirm your new wallet, "
                                 "then enter your backup seed: ")

    print("device_token {}".format(device_token))


# Cool, so now when execution continues, we'll have a device_token authorized on
# our app, so we can authenticate as the user!

# We're gonna want to save those creds,
# * particularly the device_token and backup_seed *

yn = raw_input("\nSave your credentials to ~/.gemwallet? [y/N]: ")
if yn.lower() == 'y':
    move(config_filename, "{}.bak".format(config_filename))
    fh = open(config_filename, 'w')
    fh.write(("-a{}\n"
              "-d{}\n"
              "-e{}\n"
              "#backup seed:{}").format(
                  api_token, device_token, email, backup_seed))
    fh.close()

user = client.authenticate_device(api_token=api_token,
                                  device_token=device_token,
                                  email=email)

# Now for the fun stuff.
def print_wallet(fetch=True):
    headers = ['#', 'Account', 'Network', 'Confirmed', 'Pending', 'Available']
    try:
        count = 1
        table = []
        for name, account in user.wallet.accounts.iteritems():
            if fetch:
                account = account.refresh()
            table.append([ count, name, account.network,
                           account.balance,
                           account.pending_balance,
                           account.available_balance ])
            count += 1
        print("\n" + tabulate(table))
    except Exception as e:
        print(e)

print_wallet()

def select_account():
    print_wallet(False)
    acct_number = raw_input("\nEnter account number> ")
    return user.wallet.accounts.values()[int(acct_number) - 1]

NETWORKS = ['bitcoin', 'bitcoin_testnet', 'litecoin', 'dogecoin']
def select_network():
    prompt = "What kind of account?"
    for i,v in enumerate(NETWORKS):
        prompt = ("{}\n"
                  "{}. {}").format(prompt, i + 1, v)

    acct_number = raw_input("{}\n"
                            "> ".format(prompt))

    return NETWORKS[int(acct_number) - 1]

def process_command():
    command = raw_input("""
Choose an action:
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
        print_wallet()
        return None

    if command < 5:
        account = select_account()

    if command == 1:
        if user.wallet.is_locked():
            # unlocking a user wallet decrypts the primary private key
            # used to make signatures.
            passphrase = getpass()
            user.wallet.unlock(passphrase)

        dest_address = raw_input("\nDestination address: ")
        amount = raw_input("\nTransaction amount (satoshis): ")
        tx = account.pay(payees=[dict(address=dest_address, amount=int(amount))],
                         utxo_confirmations=1)
        pop_a_browser(tx.mfa_uri)

    elif command == 2:
        # Generating an address is eeeeeasy
        print("Pay into this address: {}".format(
            account.addresses.create()['string']))
        raw_input("Press enter to continue or CTRL-C to quit")

    elif command == 3:
        for tx in account.transactions():
            pp(tx.attributes)

    elif command == 4:
        for tx in account.transactions(type='outgoing',
                                       status=['unsigned', 'unapproved']):
            tx.cancel()

    elif command == 5:
        network = select_network()
        name = raw_input("Account name> ")
        user.wallet.accounts.create(name=name, network=network)
        print_wallet()
    else:
        # wat?
        print("\n[ Unknown command ]")
        print_wallet()
    print

# off to the races! we hope...
while True:
    try:
        process_command()
    except Exception as e:
        print("Uh oh... something broke? {}\n".format(e.message))
