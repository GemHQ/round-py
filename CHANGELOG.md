
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
