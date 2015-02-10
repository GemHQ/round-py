# unit/helpers.py
#
# Copyright 2014 BitVault, Inc. dba Gem
#
# Broken out of fixtures.py so that in the future they can be used in the
# tests as well.

import pytest
import time
import httplib
import urllib

def round_url():
    return u"https://api-sandbox.gem.co:443"

def timestamp():
    return time.time()

def email():
    return u'test-{}@gem.co'.format(timestamp())

def passphrase():
    return u'incredibly_secure'

def app_name():
    return u'test-app-{}'.format(timestamp())

def instance_name():
    return u'test-instance-{}'.format(timestamp())

def wallet_name():
    return u'my favorite wallet'

def account_name():
    return u'super duper account'

def random_wallet_name():
    return u'random wallet {}'.format(timestamp())

def random_account_name():
    return u'random account {}'.format(timestamp())

def pubkey():
    return u'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAoVw+yyLfmMRSuQcUAQFK\n7I4hLYXnpt23Avl/jmHqH50HU4PiOUKSBqwoCzu6jgOzZMcZoZV5Hor86czaASqN\nJPjSVnJDmh7nav2S6IzZ7nbXI/OT26JZgtr1jieaH++o2+aV47u/tK1wPyGPM+8D\n8XpojxPOgoihNg8kXRwng6SAmqXp94Kny019qvyvjJkvM+PxehhrS1s3jv59d7NF\nbYRZlTkj9ZfXlacVcK70LfdCrdUfU2AFB4v4zHnPoEO7jGCODtXAi7PlR/nVLD36\nMGy548ozpiYI0yyM3+sJCig4W+GPifWUNtyrASUyU7u1frZ56QELJgJ+NFsBsR9l\nhQIDAQAB\n-----END PUBLIC KEY-----\n'

def privkey():
    return u'-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEAoVw+yyLfmMRSuQcUAQFK7I4hLYXnpt23Avl/jmHqH50HU4Pi\nOUKSBqwoCzu6jgOzZMcZoZV5Hor86czaASqNJPjSVnJDmh7nav2S6IzZ7nbXI/OT\n26JZgtr1jieaH++o2+aV47u/tK1wPyGPM+8D8XpojxPOgoihNg8kXRwng6SAmqXp\n94Kny019qvyvjJkvM+PxehhrS1s3jv59d7NFbYRZlTkj9ZfXlacVcK70LfdCrdUf\nU2AFB4v4zHnPoEO7jGCODtXAi7PlR/nVLD36MGy548ozpiYI0yyM3+sJCig4W+GP\nifWUNtyrASUyU7u1frZ56QELJgJ+NFsBsR9lhQIDAQABAoIBABRVDUyHbmlPg6Tw\n8WJXCVvZZPDZiKEMGv1y9tG4IMou/TdWzPCuJLxWgQ05T36JlNdEB0THEuX4WXoU\nZ/vxoqtf9xERgNcwwbRHk3VeGi/kJaPQE3d/c4v7jymEb/VKO5rJ6WUyySs5F4W8\n8tB2c6a/5+Dve/wSv02ShuB8pbX+lzF3Rh7VPHjonXxFWiS5FtehK/OFAmHXUTrQ\n0DlXBA2R437vVnmFORJE8HNpHabD8eYa8aoLBY7Yz8qWYxfrwde43r19rJkitS5B\neU5lGt6os4UinZ+JnfXKFjKbfb7ZAuRj3rkR+TgPvoRADyR4XKqs6fgohZzlC0Is\nP0bz15kCgYEA1siFjGtvgLowio7fM0SWadfykg1kSPa0vpPencXFtBBNaJDbz0F/\nB2kRp3TWw6g8hhBKZlWrfsFQa4R+pEbh/bRc6Edkh64VGWMNJ/2NxYAy+eB6DVl/\nFlLGI669MruPjoGe5aNTj03LoddGXS/04TyvNcDaK52KAw629+Glto8CgYEAwFNC\nSuG3qVNLv2+alvBtjJs+s0oznDJ/USwqYbSOOtr0EmjnTN1mDCT1EvTKNN24e/KE\ntzlzzvFnjWx+bysKg6Q4xIUmof5Q6f8hY/bASWdjaKjJxWNOTVnFtL/KMQDTA5X5\naBbZATB2FCNH0Xce5YYeL7m2uK1HT1ZDtOUETKsCgYEAtcz7hdU2h36SMeYnNW0b\n6DF6yHd/aGcyrJHbgC50Xyrhat4awL7OuEYORHEYjHqt6EiHwUFIrT0SRj/bNlAt\nYCM39QDhLhuDDn8SFsR/KSqPe4SvqvcTJKEhx/hTe0rZg6ViCzyJMSaHc9EVZTF/\nlNtZ7yTzRrHNrTLaWs1sCC8CgYA36z1YJl7PNa/NfnaVMly3yB+n44gz/x6zjELa\nW7QK+sSCYcv2tlzIZSp4k4IDcwAD0dSyrVq1rczs+sGcMwiAlAwJX6mG6jm+f3bG\n6OSpswzdTk40PRZ0OQjZ7/Wq39F6tm1ozVPVG7EJU+S6y4bJN4CpYbb15TPZpnxT\nKU9htwKBgDXiGEX56CbIw0O1AFfYEDCjDzG9HPcOtFjxvSLcIrBb1Yl+Tov3zgrZ\ns4HPVSGyi1d2T/ytIT0qWocrdO2YY3F9FhluzXrOcKlVBEGbyItx6gUCmepmp1dR\ndadVrwjj3IYw6Wa3z5+vzxviy3yCq/68yq5A+5mrAHF3Z1ZSDg4U\n-----END RSA PRIVATE KEY-----\n'

def api_token():
    return u'ssgPhVv-Pv-soqQtRM7pIFHzg7uGOGFzrAfSBVONqgo'

def user_token():
    return u'0x20mNTVcUWujHrtGENR9NjSF0_K6JYLlDfMTMUjh-Q'

def device_id():
    return u'joshua+userJava06@gem.codevice6'

def user_url():
    return u'https://api-sandbox.gem.co/users/1bIKvHKszboJhLBr2PfLLA'

def email():
    return u'joshua+userJava06@gem.co'

def instance_id():
    return u'DE73gGgLcJB07D0gW0G3VUN3aywgcd1T8F3bT-0eTy8'

def app_url():
    return u'https://api-sandbox.gem.co/apps/oHgM6NrHq-C_K2-f1pfwIg'

def dev_email():
    return u'joshua+devJava1@gem.co'

def payee(address, amount):
    return {'address':address, 'amount':amount}

def create_payees(account, num):
    amount = 20000
    payees = []
    for x in xrange(num):
        payees.append(payee(account.addresses.create().string, amount))

def getMoney(address):
    params = urllib.urlencode({'address': address})
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
    conn = httplib.HTTPConnection('faucet.haskoin.com:80')
    conn.request("POST", "/?",params,headers)
    response = conn.getresponse()
    print address, response.status, response.reason
    conn.close()

