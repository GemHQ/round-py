
0.9.4 / 2015-08-17
==================

  * Support for application wallet management through the CLI
  * Wallet.pay now supports paying from all accounts without specifying explicit payer values
  * Support application wallets in the CLI
  * Added `balances_at` which queries for balance as a function of required confirmations
  * Added support for wallet and account_query (to reduce unnecessary list calls)
  * Added netki support!
  * Backporting cacheable from 0.10.0
  * Replaced print statements with logging
  * Minor bugfixes

0.9.3 / 2015-08-05
==================

  * provider user, wallet, and account calls that accept a key parameter for notification convenience
  * pad pyotp tokens to six characters

0.9.2 / 2015-07-24
==================

  * Default to encrypting with AES+SHA256HMAC - NaCl will be removed in 0.9.3
  * Make with_mfa accept callables from anywhere
  * Memoize addresses - added account.get_addresses to provide an optional refresh (fetch) parameter

0.9.1 / 2015-07-14
==================

  * wallet.pay exists now

0.9.0 / 2015-06-04
==================

  * Python3.3+ compatible!
  * Support Gem's new key encryption scheme (no more libsodium!)

0.8.3 / 2015-06-25
==================

  * Accept an optional encrypted_seed parameter in unlock to allow applications to store their own primary private keys.

0.8.2 / 2015-06-19
==================

  * Bugfix: Use NaclPassphraseBox to create users for 0.8.x (was using the ppbox from 0.9.x)

0.8.1 / 2015-06-17
==================

  * Backporting py3 support from 0.9.0
  * Allow `account.pay` to take a callable instead of a string for `mfa_token`
  * Support old and new encryption schemes

0.8.0 / 2015-05-26
==================

  * support for litecoin and dogecoin!
  * removed network references and disabled sig_hash checking until we can eliminate python-bitcoinlib in coinop
  * removed old user.wallets accessor
  * various improvements and bug fixes
  * examples/cli.py opens a browser for you when necessary

0.7.4 / 2015-05-13
==================

  * various improvements and bug fixes
  * new Error classes in the public interface

0.7.3 / 2015-04-29
==================

  * Added simple little CLI sample project
  * Updated client to work with the new authorization_request flow
  * Reordered some parameters for consistency
  * Users are limited to one wallet. (accessible through user.wallet)
  * account.transactions now accepts a list of acceptable statuses as filters
  * Various minor improvements and bug fixes


0.7.2 / 2015-04-17
==================

  * Proper handling of Application wallets
  * Added user.devices
  * Added send_mfa and verify_mfa to User objects, for arbitrary MFA through Gem
  * instance_id/instance_token normalized to new name: admin_token
  * Cleaned up the context parameter storage in Context
  * Various minor improvements and bug fixes

0.7.1 / 2015-04-02
==================

  * Updated with the live sandbox URL!
  * Minor tweaks

0.7.0 / 2015-04-01
==================

  * TOTP support for Applications
  * Wallets.generate can provide arbitrary trees for a wallet
  * A _useful_ README
  * Docstrings!
  * New transaction flow supporting MFA
  * Eliminated the 'payments' abstraction
  * Backup seed generation for User accounts removed
  * Various bug fixes and minor improvements

0.6.2 / 2015-03-04
==================

  *  PyNaCl 0.3.0 is released :)
  *  Update README with easier install instructions
  *  Begin documentation for public release
  *  Minor bugfixes

0.6.1 / 2015-03-02
==================

  *  tweak to linux install instructions
  *  Added subscription support (event notifications)
  *  Added confirmations parameter to account.pay
  *  updated readme with better linux installation instructions

0.6.0 / 2015-02-16
==================

  * Renamed users.create(wallet to users.create(default_wallet
  * Cleanup
  * Added client-side unit tests

0.5.5 / 2015-01-27
==================

  * Moved begin_ and complete_device_authorization to the client object and require the user email address as a parameter (also renamed `name` argument to `device_name` for clarity)
  * Updated README with Heroku/Mac OS X install instructions

0.5.4 / 2015-01-12
==================

  * Remove privkey from parameters to prevent patchboard from sending it in dev.create requests
  * Fix for setting mainnet params in pycoin

0.5.3 / 2014-12-29
==================

  * Set default sandbox url to api-sandbox.gem.co
  * Added exception for locked wallets
  * added client.developer test
  * added test_authenticate_otp
  * Added authenticate_device
  * removed unnecessary default credential from otp
  * added authenticate_application -- packaged client tests will minimally interact with the API and will be limited to unit tests. Functional client testing will be maintained in-house (as it requires access to a development instance of the API)
  * started adding auth_app, but need to find an API mocking system before continuing
  * working baseline tests
  * renamed global patchboard object to reflect what it actually is
  * added UnknownNetworkError
  * support running clients against multiple urls with the same python process
  * removed old scripted tests

0.5.2 / 2014-12-04
==================

  * fixed edge case for client.user()
  * added AuthenticationError
  * reverted unnecessary timestamp param
  * removed user.applications method. Is not a thing.

0.5.1 / 2014-12-02
==================

  * switched to data-persistent developer sandbox API instance
  * users are limited to a maximum of 5 pending device authorizations
  * complete_device_authorization will return a new, valid otp key if given an expired key
  * begin/complete_device_authorization have useful errors
  * users.create and wallets.create accept either a passphrase or a pre-generated CoinOp wallet object
  * cleanup and bugfixes
    * user email query
      * client.user is no longer a property and must be called with parens
      * accepts an optional email parameter for instantiating a user object to use with begin/complete_device_authorization
    * authentication parameters
      * more/most arguments are required
      * removed app_url from authenticate_device and added user_email
    * formatting
  * deprecated multiple-authentication syntax
  * added timestamp argument for developer auth - make sure your system is syncing with a time server!

0.5.0 / 2014-11-29
==================

  First alpha release
