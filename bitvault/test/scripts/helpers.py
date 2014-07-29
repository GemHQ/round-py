# scripts/helpers.py
#
# Copyright 2014 BitVault.


import sys
from urlparse import urlparse

from patchboard import discover
from bitvault import Context


def bitvault_url():
    try:
        _script, url = sys.argv
        return url
    except:
        return "http://api.bitvault.io"


def wallet_file():
    p = urlparse(bitvault_url())
    return "demo-{0}.yaml".format(p.hostname)


def bitvault():
    return discover(bitvault_url(), {'default_context': Context()})
