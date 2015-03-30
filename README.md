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
1. [Introduction](README.md#Introduction)
1. [Run the client](README.md#Run-the-Client)
1. [Configure your application and API token](README.md#Configure-your-application-and-API-Token)
1. [Create your User and Wallet](README.md#Create-your-User-and-Wallet)
1. [Authenticate your User](README.md#Authenticate-your-User)
1. [Access the wallet and create an account](README.md#Access-the-Wallet-and-Create-an-Account)
1. [Generate an Address and Add Funds](README.md#Generate-an-Address-and-Add-Funds)
1. [Make a Payment](README.md#Make-a-Payment)
1. [Advanced Topics](README.md#advanced-topics)
	1. [More about Accounts]
	1. [More about Txs]
	1. [Subscriptions]
	1. [Integrated 2FA]
	1. [Operational/Custodail wallet models]
	1. [Operational/Custodial payments]

### Introduction
This tutorial will have you run through setting up your application and creating your own wallet as a user of your application.  By the end of the tutorial, you will have created your User, wallet, account, an address as well as fund it and then make a payment using the bitcoin testnet network.

This tutoril assumes that you have completed the developer signup and that you have successfully [installed the client](docs/install.md)

### Run the Client
In this step you will learn how to instantiate the API client for the given networks.

1. start an interactive shell and import the round library

	```bash
	$ bpython
	>>> import round
	```

1. Create the client object 

	```python 
	# the default client is set to sandbox the testnet stack 
	client = round.client()

	# if you want to configure the client for production mainnet
	client = round.client("production")
	```

### Configure your applicaiton and API Token
In this step your application and you will retrieve the API Token for the application and set your applications redirect url.  The url is used to push the user back to your app after they complete an out of band challange.

1. Set the redirect url by clicking in the options gear and selecting `add redirect url`

1. In the [console](https://my.gem.co) copy your api token down by clicking on show

1. Go back to your shell session and set a variable for api_token

	```python
	api_token = u'q234t09ergoasgr-9_qt4098qjergjia-asdf2490'
	```

### Create your User and Wallet


### Authenticate your User
### Access the wallet and create an account
### Generate an address and Add Funds
### Make a Payment
### Advanced Topics
