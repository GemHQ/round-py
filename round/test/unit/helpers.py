# unit/helpers.py
#
# Copyright 2014 BitVault, Inc. dba Gem
#
# Broken out of fixtures.py so that in the future they can be used in the
# tests as well.

import pytest
import time

def round_url():
    return u"https://api-develop.gem.co"

def timestamp():
    return int(round(time.time()))

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

def pubkey():
    return u'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4BbS/GI9R3XnLphBoYGS\n1TWWORxD1InKSwiIE3ZFx7WXGz52C8Xzo+Zagy2Pb86C6iKq2k66Xkj1UGBJD2P6\n9Tpg5TBEoArb+kD5hkkw+Ta39n/TM/VqbfAiV1iAR6i2+TGTrCWiT1IRHvTG/do/\nXD+ESRYH9W/ppAoLCpniS5vOx+Bb3nYq7RCo+ESVjDPSjgcASqXVdVBues8O2iua\nStc8oepJBNReZ5eWKkOl3ST2C9SiUsmzLrnBDVDlq0fB13ruhG7eWevP09pNMRBZ\nd8HB9AlZiaPA82PNPKj38xOBUKi51gIYoEphCPtbicWe2T/tFvpNNXHQi98nE43o\nOQIDAQAB\n-----END PUBLIC KEY-----\n'

def privkey():
    return u'-----BEGIN RSA PRIVATE KEY-----\nMIIEpQIBAAKCAQEA4BbS/GI9R3XnLphBoYGS1TWWORxD1InKSwiIE3ZFx7WXGz52\nC8Xzo+Zagy2Pb86C6iKq2k66Xkj1UGBJD2P69Tpg5TBEoArb+kD5hkkw+Ta39n/T\nM/VqbfAiV1iAR6i2+TGTrCWiT1IRHvTG/do/XD+ESRYH9W/ppAoLCpniS5vOx+Bb\n3nYq7RCo+ESVjDPSjgcASqXVdVBues8O2iuaStc8oepJBNReZ5eWKkOl3ST2C9Si\nUsmzLrnBDVDlq0fB13ruhG7eWevP09pNMRBZd8HB9AlZiaPA82PNPKj38xOBUKi5\n1gIYoEphCPtbicWe2T/tFvpNNXHQi98nE43oOQIDAQABAoIBAQC5GkFn1uJVgA/Z\nzk0QUs7uLViMjkt9aeBfAIoewWi8ocRS7dJmwToTHfmQN/cu3QAI1WAZ+kQ6E7wH\ni7Ft9CFdpb5aMvfM14uD+V3kTdsVUNy+0jGszsD+VQiY6/Lyvmt+BjS8U03yhZC8\n6GbjU/9YfOMR2A/07l+pb95VAG4MEvh3RZEIWJsOGF6f3+pvCy9RFHOSS+IdKq8N\nrbgAQ0QXBY96tP/Wj+PCyzgkgBbu2Qsv1sBzmfpaap2VqJX1yGKq4vt9kBXr4X4P\n+bHSCa86rN9BmFiV2dgQvjHkFVtA1XU8T6u9aE8/SFseEf2CSEhviVMGnnh4nHXz\nyoDphZrtAoGBAP1dvUh6uvdTeRBVwDvUavZqKvhdPxIE4T4SzMD4aThB1kGVg6pO\nZA0j8OFZsSiE+nAdgPzsuQsgrfv4pMSxkjiIj9MNx7GYtzY2OwM94/TNXW73WRQl\n+TFVBMDOrlFlFitUa84bC1B927LUpbB8D5Z7qUyFKsXoJaKFEkAHFO+fAoGBAOJr\nLCiW+IY3MNozO8ijvZM0aDZB/EVe57ppz9He7OiP5KW39EzuzJ1szDAhzyjbm0Pg\nw7XrfBfNVLQ2HoS3TdQ8mHGqE8lNDUPjPhUKDxnd2MYr/mpjL8UzATM+RclriTss\nZdD22wKuMVNa7A8p2V+LRo308gLpJ1HnV2svHTknAoGBAIK8kQRKWBlxGCImrVfy\nBvN52wxnSTkqDXPzTXYxeFHQHxeeZ99ELfpd1ljh6DlJTNT3VGyuVdl5Fm3TYmog\nWpwTU2uLS8THUZqGpzLIB810/sZYmb18zrX28cnvnCFh8OuQ10P1zoPNPcVsVsbX\nbU+wJa7XdDfEz06qLb2eKd5vAoGBAITzr6tp8ydEsz/9g6ZuV7xfsq3hk1Pcxa+V\nwH2ZLH3nOLkCysZ+FtJ992xv/egdBBAYpHNngqerX4iumr8Nr/rnVhCwcQvsXdS2\nVFcgX/utZEQBw1QPSBbAu3yunWYH6j4/9M1+lt39EWPD6QeCaG0NKHHlGlMRO5CB\niriaostTAoGAIinoiW4rwyfgXfoHRZdIsDijeVVzu1ysaVB0Wa3cqkAYHUniVBv/\nX+6D/K2O0gn7zdvvazgJZ9yFUJVJIT1nc/eLnOvMydTkdvZbbQQ06f+70ux1LNL+\na0H6Bm+s/8apvbQW6oyhzUMybu7/LLnihfLEEqDLuE8btD5SKCZz5xQ=\n-----END RSA PRIVATE KEY-----\n'
