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
* `account.pay(payees,confirmations,redirect_url)`: send bitcoin out of an account **must call [wallet.unlock()](advanced.md#wallets) first**
* `account.transactions`: return the collections of transactions

A pending_balance in Gem is any address involved in a transaction with 0 confirmations.  This means that in multiple transactions both incoming and outgoing will produce a net pending_balance.  As they confirm with a single confirmation, the account balance in the API reflects the change.  Objects get cached for speed in the client, so to fetch a new state of an account on the API, call account = account.refresh().

## Transactions and Payments
Transaction collections have a relationship to an account.  When getting the transaction collection, you can specify as an argument incoming or outgoing.
`txs = account.transactions(type=‘incoming’)`

 Now lets look at a single transaction: `tx = txs[0]`

There is a lot of information on the tx.  You can call the attributes to get at the full list `tx.attributes`.  Additionally there are some convenience methods to get at key information quickly.  For example, `tx.hash` returns the transaction hash.

### Fee Estimation
Fees are estimated by requesting for an unsigned transaction from the API.  The Gem API will then lock the unspent outputs to prevent a potential double spend.  The returned unsigned transaction will have a fee in the attributes that you can then inspect.  If you decide you don't want to perform the transaction you'll have to [cancel the transaction](advanced.md#canceling-unsigned-transaction)

Example snippet to generate an unsigned transaction:

```python
account = w.accounts['default']
toAddress = u'2N4MtK1rZ88UWXDGWWVf1gYz1Runj4FMDr7'
payees = [{'address':toAddress, 'amount':483034}]
content = dict(outputs=account.outputs_from_payees(payees))
unsigned = account.resource.payments.create(content)

unsigned['fee']
```

### Canceling Unsigned Transaction
You can accomplish this by calling `tx.cancel()` on a transaction.  If you have a lot of transactions you can loop over the collection and cancel.

```python
for tx in account.transactions(type='outgoing'):
    tx.cancel() if tx.attributes['status'] == 'unsigned'
```

## Attributes and Refresh
### Attributes
All objects in the round client have attributes in a key/value store.  If you want to see information within the attributes all you have to do is access it like any k/v object.

to see all the attributes of an object:

```python
from pprint import pprint as pp
pp(account.attributes)
```
To access a particular attribute:

```python
fee = tx.attributes[u’fee’]
user_email = user.attributes[u'email']
```

__If there are no convenience methods for attributes you use often, please file an issue with what you need or make a pr if you build it in yourself.__

### Refresh()
The data on objects are cached client-side for performance versuses having to make API calls for every single method.  What this also means is that if you have for example an instance method for an account, then the information on the account could get into a stale state.  You will have to trigger a refresh of the object with any changes from the API. 

When calling refresh, the object will be returned with the updated information.  Refresh can be called on individual objects as well as the corresponding collections.  For example:

* `account = account.refresh()`: returns the account with any updated information
* `account_collection = account_collection.refresh()`: returns an updated collection

## Subscriptions
Setting up a subscription on your application will allow you to be notified via a webhook about any incoming/outgoing transaction for any address associated with an account in a wallet of your users.  There is no need to manage webhooks at an address level anymore.  Gem's API will automatically register any new address or change address added to accounts automatically.  When a subscription is triggered, Gem will attempt delivery to the provided callback_url.  If your app server does not respond with a 200, Gem will continue to try.

### Configure the Application

1.  Go to the console and add a `subscription token` to the application.  This token is shared with the API and Gem will embed the token in any subscription notification that is sent to your app.

1. Expand the application by clicking on the name.  You will see a section called “subscriptions”

1. Click the “add new subscription”  and provide the callback_url .  Any new address added to any users wallet authorized on your app will automatically registered for you.

### Webhook operations
You will start to receive a webhook subscription at the provided url for incoming/outgoing transactions.  The payload of the subscription will contain information about the transaction, amount, and UIDs for the user/wallet/account information.  You’ll be able to use this information to query your app.

For example - the following snippet will retrieve the user in a given subscription 

```python
generate the client
client = round.client()

Authenticate with application credentials
app = client.authenticate_application(app_url, api_token, instance_token)

get the user given the user key from a subscription.
sub_user_key = ‘2309rjefvgnu1340jvfvj24r0j’
user = None
for u in app.users.itervalues():
	user = u if u.attributes[u’key’] == sub_user_key
```

##  Integrated 2FA
Gem has built 2FA into the API but additionally built a system to add additional 2FA challenges to your app, so you don’t have to integrate yet another api.  You can ask Gem to send an sms challenge to the user to then pass back to your app.  The user will not get an SMS if the user has a TOTP app installed like Google Authenticator, Authy, Duo etc.  

Example of how to incorporate 2FA into your app.

```python
def login_user(user):
	user.send_mfa(phone_number = 5555551212)
	verify_password()
	unlock_account(user) if user.verify_mfa(USER_ENTERED_MFA) 
```

## Operational/Custodial Wallets
There are certain scenarios where you want to implement a wallet that you are in posession of that is used for business or custodial purposes.  In the operational/custodial model you will have two keys, the primary used for daily signing and the backup used for recovery.  This means that you hold funds be it the business or your end users.

### Configure 

* Create a new instance token in the management console.  
	* Instance tokens are used in the application authentication scheme.  When authenticating as an application, you will have full control of the applications wallets and allows a read only view of end user data if your app supports both.
* __Keep the token safe__

### Authenticate
To authenticate as an application to get to an application wallet and/or pull information about the application call:

```python
app = client.authenticate_application(app_url=app_url, 
                                      api_token=api_token, 
                                      instance_id=instance_id)
```

### Wallet creation

`backup_key, totp_secret, wallet = app.wallets.create(<PASSPHRASE>)`

* The totp secret is to be stored in a config file on the server operating the round client for this wallet.  This will be a part of the payment process.
* The backup key is the root node that can derive all accounts, addresses.  This key will only be returned once via this call.  __YOU MUST STORE IT IN A SAFE PLACE OFFLINE__.  If you loose the backup_key and then later forget the passphrase to unlock the primary key, you will not be able to recover the wallet.
* The wallet is the full wallet.  You can generate the accounts, addresses etc same as an end user in the previous steps.

### Payments
In this section you’ll learn how to make a payment for an operational/custodial wallet.

1. Authenticate as the application
	1. `app = client.authenticate_application(app_url, api_token, instance_token)`
1. Unlock the wallet.
	1. `wallet.unlock(passphrase, top_secret)`
1. make a payment
	1. `account.pay(payee,confirmations=4, app.totp_token.now())`

The Gem client will use the top_secret to generate an MFA token that will be sent as part of the payment calls and verify on the Gem API side.
