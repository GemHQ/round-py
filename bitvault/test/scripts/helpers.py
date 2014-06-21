import sys
from urlparse import urlparse

from patchboard import discover
from bitvault.client import Context

def bitvault_url():
    try:
        _script, url = sys.argv
        return url
    except:
        return "http://localhost:8999"

def wallet_file():
    p = urlparse(bitvault_url())
    return "demo-{0}.yaml".format(p.hostname)

def bitvault():
    return discover(bitvault_url(), {'default_context': Context()})


