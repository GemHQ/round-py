# scripts/helpers.py
#
# Copyright 2014 BitVault, Inc. dba Gem


import sys
from urlparse import urlparse

from patchboard import discover
from round import Context


def round_url():
    try:
        _script, url = sys.argv
        return url
    except:
        return "http://api.gem.co"


def wallet_file():
    p = urlparse(round_url())
    return "demo-{0}.yaml".format(p.hostname)


def round():
    return discover(round_url(), {'default_context': Context()})
