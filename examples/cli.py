# Hey guys, here's a quick demo of how to use Gem's python client library to
# build something awesome and quick. Below I've outlined the specs for a simple
# CLI wallet app.
#
# round-cli: A super simple command-line bitcoin wallet to show off Gem's API!
#
# Requirements:
# - A user can create a new Gem multisig wallet
# - A user can log into an existing Gem multisig wallet.
# - A user can get an address to receive bitcoin
# - A user can send bitcoin to any address.
#
# First! We need to install the round package through pip.
# And after that, we'll need a developer account. That'll take a second, so
# let's grab the API Token from the dev console (sandbox.gem.co)
#

# Every CLI needs argument parsing:
import argparse
from getpass import getpass #secure password entry

import round # woo!

API_TOKEN = 'C5Y2bFRPy9UgfEm8SlmJjkc3SnInDMAwlmhNCmkeTOo' #we'll need this


parser = argparse.ArgumentParser(
    description="A simple Gem-back command-line bitcoin wallet.")
parser.add_argument('email', help="Your email address")
parser.add_argument('-d', '--device_token', help="Your device_token")
args = parser.parse_args()

email = args.email
print "Enter your passphrase or pick a new one if you don't have an account yet!"
passphrase = getpass()


# Now we need a client to talk to Gem.
# I'm hitting our development stack to avoid cluttering the sandbox logs,
# You can omit the url parameter and just do `round.client()`
client = round.client(url="http://api-develop.gem.co")

# Now we have to authenticate before sending requests:
client.authenticate_identify(API_TOKEN)

# If they pass a device_token in the arguments as above (-d) then we assume
# they have an account.
if args.device_token:
    device_token = args.device_token
else:
    try:
        # Let's try to get an existing user first. It'll throw an exception
        # if the account doesn't exist.

        user = client.user(email) # wow, such difficult

        # Since we don't have a device_token from them, we'll need to create
        # A new user device to associate our app with their account.
        device_token, mfa_uri = user.devices.create(name="Gem CLI")

        # Then they can visit the mfa_uri we receive back to authorize with their
        # 2FA authorization code.
        print "Open this URL in your web browser to authorize this device: \n{}".format(mfa_uri)
    except:
        # Whoops, looks like they don't have an account! Let's make one.
        device_token = client.users.create(email=email,
                                           passphrase=passphrase,
                                           device_name="Gem CLI")
        raw_input("Check your email to confirm your new wallet, then press enter")

# Cool, so now when execution continues, we'll have a device_token authorized on
# our app, so we can authenticate as the user!

# We're gonna want to save that backup seed!
# phone dragon region unique region just hockey develop tag neutral secret tooth chest moon pipe guitar drip during present moon chat nature ball diesel
# The device token would be good too: BWpo7FUpea6k969E7eX5Dm75rRwaY49CIBG9XbWcE-E

print "Store this device_token (if you lose it you'll have to authorize a new app):"
print device_token
user = client.authenticate_device(api_token=API_TOKEN,
                                  device_token=device_token,
                                  email=email)

# Now for the fun stuff.
def print_wallet(user):
    user.refresh()
    # I wrote this beforehand:
    print "\n{}, your wallet has a balance of {} satoshis".format(
        user.first_name, user.wallet.balance)

    print "Account \t Balance (satoshis)"
    for name, account in user.wallet.accounts.iteritems():
        print "{} \t {}".format(name, account.balance)

print_wallet(user)

def process_command():
    command = raw_input("""
Choose an action:
1. Send bitcoin
2. Receive bitcoin (generate a new address)
> """)

    # For this version we'll assume they want to use the default account.
    if command == '1':
        if user.wallet.is_locked():
            # unlocking a user wallet decrypts the primary private key
            # used to make signatures.
            user.wallet.unlock(passphrase)

        dest_address = raw_input("destination address> ")
        amount = raw_input("Transaction amount (satoshis) >")
        tx = user.wallet.accounts['default'].pay(payees=dict(address=dest_address,
                                                             amount=amount))
        print "\nVisit this URL to authorize this transaction:\n\t{}".format(
            tx.mfa_uri)
        raw_input("Press enter to continue or CTRL-C to quit")

    elif command == '2':
        # Generating an address is eeeeeasy
        print "Pay into this address: {}".format(
            user.wallet.accounts['default'].addresses.create()['string'])
        raw_input("Press enter to continue or CTRL-C to quit")
    else:
        # wat?
        print "[ Unknown command ]"
        print_wallet(user)
    print

# off to the races! we hope...
while True:
    try:
        process_command()
    except Exception as e:
        print "Uh oh... something broke? {}".format(e.message)
