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
from json import dumps, loads
from os.path import expanduser
import round # woo!


parser = argparse.ArgumentParser(
    description="A simple Gem-back command-line bitcoin wallet.")
parser.add_argument('email', help="Your email address")
parser.add_argument('-a', '--api_token', help="Your api_token")

parser.add_argument('-u', '--url',
                    help="Gem API URL (https://api-sandbox.gem.co)",
                    default="https://api-sandbox.gem.co")

parser.add_argument('-d', '--device_token',
                    help="Your device_token",
                    default=None)
args = parser.parse_args()

# try:
#     fh = open("{}/.gemcli".format(expanduser('~')), 'r')
#     confargs = loads(fh.read())
#     fh.close()
# except:
#     confargs = {}


api_token = args.api_token
device_token = args.device_token
url = args.url

# if 'email' in confargs and args.email == confargs['email']:
#     if 'device_token' in confargs:
#         device_token = confargs['device_token']
#     if 'api_token' in confargs:
#         api_token = confargs['api_token']

email = args.email

# Now we need a client to talk to Gem.
client = round.client(url=url)

# Now we have to authenticate before sending requests:
client.authenticate_identify(api_token)

if not device_token:
    try:
        # Let's try to get an existing user first. It'll throw an exception
        # if the account doesn't exist.
        user = client.user(email) # wow, such difficult

        # Since we don't have a device_token from them, we'll need to create
        # A new user device to associate our app with their account.
        device_token, mfa_uri = user.devices.create(name="Gem CLI")

        # Then they can visit the mfa_uri we receive back to authorize with their
        # 2FA authorization code.
        raw_input("Open this URL in your web browser to authorize this device, then press enter: \n{}".format(mfa_uri))
    except:
        # Whoops, looks like they don't have an account! Let's make one.
        print "Pick a secure passphrase > "
        passphrase = getpass()
        device_token = client.users.create(email=email,
                                           passphrase=passphrase,
                                           device_name="Gem CLI")
        backup_seed  = raw_input("Check your email to confirm your new wallet, then enter your backup seed > ")

    print "device_token {}".format(device_token)

# Cool, so now when execution continues, we'll have a device_token authorized on
# our app, so we can authenticate as the user!

# We're gonna want to save those creds,
# * particularly the device_token and backup_seed *

# yn = raw_input("Save your credentials to ~/.gemcli? [Y/n] ")
# if yn.lower() == 'n':
#     print "okay, but don't lose them! Here's your device_token:\n {}".format(device_token)
# else:
#     fh = open('{}/.gemcli'.format(expanduser('~')), 'w')
#     fh.write(dumps(confargs))
#     fh.close()

user = client.authenticate_device(api_token=api_token,
                                  device_token=device_token,
                                  email=email)

# Now for the fun stuff.
def print_wallet(user):
    print "Account \t\t Balance \t Pending Balance"
    for name, account in user.wallet.accounts.iteritems():
        account = account.refresh()
        print "{} \t {} \t {}".format(name,
                                      account.balance,
                                      account.pending_balance)

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
            passphrase = getpass()
            user.wallet.unlock(passphrase)

        dest_address = raw_input("destination address> ")
        amount = raw_input("Transaction amount (satoshis) >")
        tx = user.wallet.accounts['default'].pay(payees=[dict(address=dest_address,
                                                              amount=int(amount))],
                                                 utxo_confirmations=1)
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
