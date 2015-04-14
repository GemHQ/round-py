
0.6.3 / 2015-04-14
==================

  *  updated DEFAULT_URLs to the point to the legacy stack (round <= 0.6.x is legacy and will not work with api.gem.co or api-sandbox.gem.co)
  *  client.user always creates a wrapped UserQuery if email parameter is present
  *  client.user takes an optional fetch boolean parameter (default True) which controls whether user.refresh() is run

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
