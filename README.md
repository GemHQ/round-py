# round-py: A Python client for the Gem API
The round client is designed to interact with Gem's API to make building blockchain apps drop dead simple.  All the complexity of the bitcoin protocol and crypto has been abstracted away so you can focus on building your product.  Here are a few of the many great things the API and clients provide:

* Multi-signature wallets with Gem as a cosigner
* Webhook notifications automatically subscribed for you
* Integrated 2FA solution with arbitrary endpoints to build into your app
* Simplified balance inqueries
* Easy address management
* Hardware Security Modules for co-signing key
* Rules engine for transactions
* SDKs for many popular languages

## Support information
* __Support email__: [support@gem.co](mailto:support@gem.co) 
* __Support IRC chat__: `#gemhq` on `irc.freenode.net`
* __Issues__:  Use github issues
* __Slack room__:  Send email to support requesting access to the slack room for this client
* __Detailed API Docs__:  http://guide.gem.co

## Installing round-py:
### Prerequisites:
* Python 2.7
* Virtualenv and virtualenvwrapper (or equivalent virtual environment solution) is required for Linux and recommended for everyone.
* Git and a python extension build environment.
* libffi

#### [Linux (debian-based, tested on Ubuntu 14.04)](docs/install.md#linux-debian-based-tested-on-ubuntu-1404)
#### [Mac OSX](docs/install.md#Mac-OSX)
#### [Heroku](docs/install.md#Heroku)

## Getting Started Tutorial
#### Table of Contents
* [Introduction](README.md#Introduction)
* [1. Run the client](README.md#Run-the-Client)
* [2. Configure your application and API token](README.md#Configure-your-application-and-API-Token)
* [3. Create your User and Wallet](README.md#Create-your-User-and-Wallet)
* [4. Authenticate your User](README.md#Authenticate-your-User)
* [5. Access the wallet and Default Account](README.md#Access-the-Wallet-and-Default-Account)
* [6. Generate an Address and Add Funds](README.md#Generate-an-Address-and-Add-Funds)
* [7. Make a Payment](README.md#Make-a-Payment)
* [Advanced Topics](README.md#advanced-topics)
	* [More about Wallets and Accounts](docs/advanced.md#wallet-and-account-details)
	* [More about Txs](docs/advanced.md#Transactions)
	* [Subscriptions](docs/advanced.md#Subscriptions)
	* [Integrated 2FA](docs/advanced.md#2FA)
	* [Operational/Custodail wallet models](docs/advanced.md#Operational-Custodial-Wallets)
	* [Operational/Custodial payments](docs/advanced.md#Operational-Custodial-Wallet-Payments)

### Introduction
This tutorial will have you run through setting up your application and creating your own wallet as a user of your application.  By the end of the tutorial, you will have created your User, wallet, account, an address as well as fund it and then make a payment using the bitcoin testnet network.

This tutoril assumes that you have completed the developer signup and that you have successfully [installed the client](docs/install.md)

### 1. Run the Client
In this step you will learn how to instantiate the API client for the given networks.

1. start an interactive shell and import the round library

	```bash
	$ bpython
	>>> import round
	```

1. Create the client object using the sandbox stack 

	```python 
	# the default client is set to sandbox the testnet stack 
	client = round.client()

	# if you want to configure the client for production mainnet
	client = round.client("production")
	```

### 2. Configure your applicaiton and API Token
In this step your application and you will retrieve the API Token for the application and set your applications redirect url.  The url is used to push the user back to your app after they complete an out of band challange.

1. Set the redirect url by clicking in the options gear and selecting `add redirect url`

1. In the [console](https://my.gem.co) copy your api token down by clicking on show

1. Go back to your shell session and set a variable for api_token

	```python
	api_token = u'q234t09ergoasgr-9_qt4098qjergjia-asdf2490'
	```

### 3. Create your User and Wallet
In this step you will create your own personal Gem user and wallet authorized on your application.  This is an end user account for a user to have a Gem wallet to hold bitcoin with and generate 2 of 3 keys thus the user is in full control.

1. Create your user and wallet:

	```python
	#  Store the device token for future authentication
	device_token, lite_user = client.users.create(
			first_name = "YOUR FIRST NAME",
			last_name = "YOUR LAST NAME",
			email = "YOUR EMAIL ADDRESS",
			passphrase = "aReallyStrongPassword",
			device_id = "UUID String",
			device_name = "SOME DEVICE NAME")
	```
1. **Store the device_token safety** as this will be used for subsequent login sessions with the user.
1. You will receive an email from Gem asking you to confirm your account and finish setup.  Please follow the instructions.

### 4. Authenticate your User
In this step you will learn how to authenticate a users device to get a fully functional user to perform wallet actions.  You use this call when the user returns to your app from the create step, or subsequent calls thereafter.

1. Call the authenticate_device method from the client object
	
	```python
	full_user = client.authenticate_device(
						api_token = api_token,
						device_token = device_token,
						user_email = email)
	```

### 5. Access the wallet and Default Account
In this section you'll learn how to get to the default account of a wallet.  A wallet is a collection of accounts.  [Learn more about the wallet and acocunts]([docs/wallet-and-account-details.md)

1. Get the default wallet and then default account

	```python
	my_account = full_user.wallets['default'].accounts['default']
	```

### 6. Generate an Address and Add Funds
In this section you'll learn how to create an address to fund with testnet coins aka funny money.

1. Create an address

	```python
	 address = my_account.addresses.create()
	print address.string, address.path
	```
1. Copy the address string and go to a faucet to fund it:
	1. [TP's TestNet Faucet](https://tpfaucet.appspot.com/)
	1. [Mojocoin Testnet3 Faucet](http://faucet.xeno-genesis.com/)

Payments have to be confirmed by the network and on Testnet that can be slow.  To monitor for confirmations: input the address into the following url `https://live.blockcypher.com/btc-testnet/address/<YOUR ADDRESS>`.  The current standard number of confirmations for a transaction to be considered safe is 6. 

You will be able to make a payment on a single confirmation.  While you wait for that to happen, feel free to read more details about:
[Wallets and Accounts](docs/Advanced-Topics.md#More-About-Wallets-and-Accounts)

### 7. Make a Payment
In this section you’ll learn how to create a payment a multi-signature payment in an HD wallet.  Once your address gets one more more confirmations we’ll be able to send a payment out of the wallet.  To make a payment, you'll unlock a wallet, generate a list of payees and then call the pay method.

1. Unlock the wallet:

	```python
	wallet.unlock(<YOUR PASSWORD>)
	```
1. Make a payment

	```python
	payment = account.pay([{‘address’:’ mxzdT4ShBudVtZbMqPMh9NVM3CS56Fp11s’, ‘amount’:25000}],confirmations = 1, ‘https://my.mobileapp.com')
	```

the pay call takes a list of payee objects.  A payee is a dict of `{'address':ADDRESS, 'amount':amount}` where address is the bitcoin address and amount is the number of satoshis.  Confirmations default to six and represents the number of confirmations an unspent output needs to have in order to be used in the transaction.  The last arg is the redirect url for Gem to send the user back to your application after the user submits their 2FA challenge.  

**CONGRATS** - now build something cool. 
