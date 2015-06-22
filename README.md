# round-py: A Python client for the Gem API
The round client is designed to interact with Gem's API to make building blockchain apps drop dead simple.  All the complexity of altcoin protocols and cryptography has been abstracted away so you can focus on building your product.  Here are a few of the many great things the API and clients provide:

* Multi-signature wallets with Gem as a cosigner
* Bitcoin, Testnet, Litecoin, and Dogecoin support (multisig for all!)
* Webhook notifications automatically subscribed for you
* Integrated 2FA solution with arbitrary endpoints to build into your app
* Simplified balance inqueries
* Easy address management
* Hardware Security Modules for co-signing key
* Rules engine for transactions
* SDKs for many popular languages

## Support information
* __Support email__: [support@gem.co](mailto:support@gem.co)
* __Issues__:  Use github issues
* __Slack room__:  Send email to support requesting access to the slack room for this client
* __Detailed API Docs__:  [Gem API Docs](http://guide.gem.co)

## Installing round-py:
### Prerequisites:
* Python 2.7/3.3+
* Git
* [virtualenv](http://pypi.python.org/pypi/virtualenv)/[virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) or a similar virtual environment solution is recommended. (`sudo` is bad)

#### [Linux (debian-based, tested on Ubuntu 14.04)](docs/install.md#linux-debian-based-tested-on-ubuntu-1404)
#### [Mac OSX](docs/install.md#mac-osx)
#### [Windows](docs/install.md#windows)
#### [Heroku](docs/install.md#heroku)

## Getting Started Tutorial
#### Table of Contents
* [Introduction](README.md#Introduction)
* [1. Run the client](README.md#1-run-the-client)
* [2. Configure your application and API token](README.md#2-configure-your-application-and-api-token)
* [3. Create your User and Wallet](README.md#3-create-your-user-and-wallet)
* [4. Authenticate your User](README.md#4-authenticate-your-user)
* [5. Access the wallet and Default Account](README.md#5-access-the-wallet-and-default-account)
* [6. Generate an Address and Add Funds](README.md#6-generate-an-address-and-add-funds)
* [7. Make a Payment](README.md#7-make-a-payment)
* [Advanced Topics](docs/advanced.md)
    * [More about Wallets and Accounts](docs/advanced.md#wallets-and-accounts)
    * [More about Transactions](docs/advanced.md#transactions-and-payments)
    * [Subscriptions](docs/advanced.md#subscriptions)
    * [Integrated 2FA](docs/advanced.md#integrated-2fa)
    * [Operational/Custodail wallet models](docs/advanced.md#operationalcustodial-wallets)
    * [Operational/Custodial payments](docs/advanced.md#payments)

### Introduction
This tutorial will have you run through setting up your application and creating your own wallet as a user of your application.  By the end of the tutorial, you will have created your User, wallet, account, an address as well as fund it and then make a payment using the bitcoin testnet network.

This tutorial assumes that you have completed the developer signup and that you have successfully [installed the client](docs/install.md)

### 1. Run the Client
In this step you will learn how to instantiate the API client for the given networks.

1. start your favorite interactive shell and import the round library

    ```bash
    $ python
    >>> import round
    # If you need access to the round builtin, then import as something else:
    >>> import round as gemlib
    # Or just import the client factory:
    >>> from round import client
    ```

1. Create the client object using the sandbox environment

    ```python
    # the default client is set to sandbox (the testnet environment)
    client = round.client()
    ```

[[top]](README.md#getting-started-tutorial)

### 2. Configure your applicaiton and API Token
In this step your application and you will retrieve the API Token for the application and set your applications redirect uri.  The uri is used to push the user back to your app after they complete an out of band challenge.

1. Set the redirect uri by clicking in the options gear and selecting `add redirect_uri`

1. In the [console](https://sandbox.gem.co) click `show` to copy your api_token.

1. Go back to your shell session and set a variable for api_token.

    ```python
    api_token = u'q234t09ergoasgr-9_qt4098qjergjia-asdf2490'
    ```

[[top]](README.md#getting-started-tutorial)

### 3. Create your User and Wallet
In this step you will create your own personal Gem user and wallet authorized on your application.  This is an end-user account, which will have a 2-of-3 multisig bitcoin wallet.

1. Create your user and wallet:

    ```python
    #  Store the device token for future authentication
    device_token = client.users.create(
        first_name = "YOUR FIRST NAME",
        last_name = "YOUR LAST NAME",
        email = "YOUR EMAIL ADDRESS",
        passphrase = "aReallyStrongPassphrase",
        device_name = "SOME DEVICE NAME",
        api_token = "YOUR API TOKEN",
        redirect_uri = "http://optional-uri/user-device-approved")
    ```

1. Your application should **store the device_token permanently** as this will be required to authenticate from your app as this user. If you lose it, you will have to create a new device for the user to authorize. (`device_token, mfa_uri = user.devices.create(name)` - the mfa_uri is where you redirect the user to provide their confirmation token.)
1. You will receive an email from Gem asking you to confirm your account and finish setup.  Please follow the instructions. At the end of the User sign up flow, you'll be redirected to the redirect_uri provided in users.create (if you provided one).

[[top]](README.md#getting-started-tutorial)

### 4. Authenticate your User
In this step you will learn how to authenticate to the Gem API on a User's device to get a fully functional User object with which to perform wallet actions.

1. Call the authenticate_device method from the client object

    ```python
    full_user = client.authenticate_device(
        api_token = api_token,
        device_token = device_token,
        email = email)
    ```

[[top]](README.md#getting-started-tutorial)

### 5. Access the wallet and Default Account
[Wallets and Accounts](docs/advanced.md#wallets-and-accounts)

1. Get the default wallet and then default account (which is a bitcoin account)

    ```python
    my_wallet = full_user.wallet
    my_account = my_wallet.accounts['default']
    ```

2. Or create an account...say an altcoin!

    ```python
    #network takes one of 'bitcoin', 'bitcoin_testnet', 'litecoin', 'dogecoin'
    my_account = my_wallet.accounts.create(name='brand-new-account', network='litecoin')
    ```

[[top]](README.md#getting-started-tutorial)

### 6. Generate an Address and Add Funds
In this section you'll learn how to create an address to fund with testnet coins aka funny money.

1. Create an address

    ```python
    address = my_account.addresses.create()
    print address.string, address.path
    ```
1. Copy the address string and go to a faucet to fund it:
    1. [TP's Testnet Faucet](https://tpfaucet.appspot.com/)
    1. [Haskoin Testnet Faucet](http://faucet.haskoin.com/)

Payments have to be confirmed by the network and on Testnet that can be slow.  To monitor for confirmations: input the address into the following url `https://live.blockcypher.com/btc-testnet/address/<YOUR ADDRESS>`.  The current standard number of confirmations for a transaction to be considered safe is 6.

You will be able to make a payment with only one confirmation, however.  While you wait for that to happen, feel free to read more details about:
[Wallets and Accounts](docs/advanced.md#wallets-and-accounts)

[[top]](README.md#getting-started-tutorial)

### 7. Make a Payment
In this section you’ll learn how to create a payment a multi-signature payment in an HD wallet.  Once your address gets one confirmation we’ll be able to send a payment out of the wallet.  To make a payment, you'll unlock a wallet, generate a list of payees and then call the pay method.

1. Unlock the wallet:

    ```python
    my_wallet.unlock(<PASSPHRASE>) # Same passphrase used in users.create
    ```
1. Make a payment

    ```python
    transaction = my_account.pay(
        payees=[{'address': 'mxzdT4ShBudVtZbMqPMh9NVM3CS56Fp11s', 'amount':25000}],
        utxo_confirmations = 1,
        redirect_uri='https://my.mobileapp.com/user_redirect')
    ```
1. Direct the user to the Gem multi-factor authentication(MFA) url for user to confirm the tx

   ```python
   transaction.attributes[u'mfa_url']
   ```

The pay call takes a list of payee objects.  A payee is a dict of `{'address':ADDRESS, 'amount':amount}` where address is the bitcoin address and amount is the number of satoshis.  `utxo_confirmations` default to 6 and represents the number of confirmations an unspent output needs to have in order to be selected for the transaction.  The last argument is the redirect uri for Gem to send the user back to your application after the user submits their MFA challenge.

**CONGRATS** - now build something cool.

[[top]](README.md#getting-started-tutorial)
