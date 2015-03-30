# round-py: Advanced Topics

## Wallets and Accounts

### Wallets
The wallet itself is a BIP32 hierarchical deterministic (HD) wallet.  The Gem wallet takes the approach of calling the root node a wallet.  Going to depth1 gets you to the Account nodes and depth2 the addresses underneath the accounts.  

The Gem wallet has convenience methods to make managing the wallet easy to do.  There are key methods to use off of the wallet object:

* `wallet.balance`: returns the total balance of all accounts
* `wallet.is_locked()`: returns True if locked
* `wallet.accounts`: returns a collection of round accounts.

### Accounts
A gem account is the main object to interact with.  The account is where payments are made from and where you access transaction collections.  The gem wallet can have many accounts.  As mentioned in the wallet section, a Gem account within a wallet is a collection of bitcoin addresses and the complexity of dealing with addresses is now abstracted away.  

The key methods on an account to use are:

* `account.balance`: returns the sum of all transactions with 1 or more confirmations
* `account.pending_balance`: returns the sum of all incoming outgoing transactions with 0 confirmations
* `account.pay(payees,confirmations,redirect_url)`: send bitcoin out of an account **must call [wallet.unlock](advanced.md#wallets) first**
* `account.transactions`: return the collections of transactions

A pending_balance in Gem is any address involved in a transaction with 0 confirmations.  This means that in multiple transactions both incoming and outgoing will produce a net pending_balance.  As they confirm with a single confirmation, the account balance in the API reflects the change.  Objects get cached for speed in the client, so to fetch a new state of an account on the API, call account = account.refresh().

## Transactions and Payments
Transaction collections have a relationship to an account.  When getting the transaction collection, you can specify as an argument incoming or outgoing.
`txs = account.transactions(type=‘incoming’)`

 Now lets look at a single transaction: `tx = txs[0]`

There is a lot of information on the tx.  You can call the attributes to get at the full list `tx.attributes`.  Additionally there are some convenience methods to get at key information quickly.  For example: `tx.hash`: returns the transaction hash

### Fee Estimation
Fees are estimated by requesting for an unsigned transaction from the API.  The Gem API will then lock the unspent outputs to prevent a potential double spend.  The returned unsigned transaction will have a fee in the attributes that you can then inspect.  If you decide you don't want to perform the transaction you'll have to [cancel the transaction](advanced.md#canceling-unsigned-transaction)


### Canceling Unsigned Transaction
You can accomplish this by calling tx.cancel()

### Accessing Details about the Transaction
tx.attributes[u’fee’] or tx.attributes[‘status’]

## Attributes and Refresh
If you want to see information within the attributes all you have to do is access it like any other k/v object.
tx.attributes[u’fee’] or tx.attributes[‘status’]

## Subscriptions
In this section you’ll learn how to setup subscriptions on your application to be notified of any incoming/outgoing transactions.

In the management console - add a subscription token to the application.  This token is shared with the API and Gem will embed the token in any subscription notification that is sent to your app.

Expand the application by clicking on the name.  You will see a section called “subscriptions”

Click the “add new subscription”  and that’s it.  Any new address added to any users wallet is automatically registered for you.

You will start to receive a webhook subscription at the provided url for incoming/outgoing transactions.  The payload of the subscription will contain information about the transaction, amount, and UIDs for the user/wallet/account information.  You’ll be able to use this information to query your app.
For example - the following snippet will retrieve the user in a given subscription 

generate the client
client = round.client()

Authenticate with application credentials
app = client.authenticate_application(app_url, api_token, instance_token)

get the user given the user key from a subscription.
sub_user_key = ‘2309rjefvgnu1340jvfvj24r0j’
user = None
for u in app.users.itervalues():
	user = u if u.attributes[u’key’] == sub_user_key

##  Integrated 2FA
In this section you’ll learn about how to use the Gem 2FA system to add additional 2FA challenges to your app, so you don’t have to integrate another api.

user.send_mfa()

user.verify_mfa()

developer.send_mfa(phone_overrride=True)

## Operational/Custodial Wallets
In this section you’ll learn how to setup an internal wallet that you the developer are in full control over.  This can be a custodial modal where you hold funds on behalf of your users or if you have a business wallets.

Create a new instance token in the management console.  

Instance tokens are used in the application authentication scheme.  This gives a particular client full control of the applications wallets and allows a read only view of end user data if your app supports both.

Now we can authenticate
app = client.authenticate_application(app_url, api_token, instance_token)

From here we create a new wallet.
backup_key, totp_secret, wallet = app.wallets.create(<PASSPHRASE>)

The backup key is the root node that can derive all accounts, addresses.  This key will only be returned once via this call.  YOU MUST STORE IT IN A SAFE PLACE OFFLINE.  If you loose the backup_key and then later forget the passphrase to unlock the primary key, you will not be able to recover the wallet.

The top secret is to be stored in a config file on the server operating the round client for this wallet.  This will be a part of the payment process.

The wallet is the full wallet.  You can generate the accounts, addresses etc same as you did in the previous steps.

### Authorization

### Wallet creation

### Payments
In this section you’ll learn how to make a payment for an operational/custodial wallet.

Authenticate as the application
app = client.authenticate_application(app_url, api_token, instance_token)
Unlock the wallet.
wallet.unlock(passphrase, top_secret)

make a payment
account.pay(payee,confirmations=4)

The Gem client will use the top_secret to generate an MFA token that will be sent as part of the payment calls and verify on the Gem API side.
