#!/usr/bin/env python
from pprint import pprint
import logging
import time
import pdb

logging.basicConfig(level=logging.DEBUG)

def cli_to_ipy(fn):
    d={}
    with open(fn) as f:
        for l in f.readlines():
            if l[:2] == '-a':
                d['apitoken']=l[2:-1]
            if l[:2] == '-m':
                d['admintoken']=l[2:-1]
            if l[:2] == '-d':
                d['devicetoken']=l[2:-1]
            if l[:2] == '-u':
                d['url']=l[2:-1]
            if l[:2] == '-e':
                d['email']=l[2:-1]
    return d

def gogo(context='usr'):
    d = cli_to_ipy('/Users/matt/.gemwallet')
    from round import client
    global c; global usr; global app;
    c = client(url=d['url'] if 'url' in d else None)
    try:
        if context != 'usr': raise Exception()
        usr = c.authenticate_device(d['apitoken'],d['devicetoken'],d['email'])
        print("usr: {}".format(usr))
    except:
        app = c.authenticate_application(d['apitoken'],d['admintoken'])
        print("app: {}".format(app))
### ^ jacked from .pythonrc

if __name__ == '__main__':
    global app
    gogo('app')

    rand_val = str(time.time())[-4:]
    bkup_seed, wallet = app.wallets.create(name='wallet_{}'.format(rand_val), passphrase='asdfasdf')
    wallet.unlock('asdfasdf')
    asset = wallet.assets.create(name='asset_{}'.format(rand_val))
    print('\n\nasset:\n')
    pprint(asset.attributes)

    account = wallet.accounts.create('bcy', network='bcy')

    addr = account.addresses.create()['string']
    # single-sig BCY address generated from cosigner key (not in hsm)
    print('\n\naddress:\n')
    pprint(addr)

    definition_tx = asset.issue(payees=[{'amount': 10, 'address': addr}], metadata=dict(look="data"))
    print('\n\nasset definition tx:\n')
    pprint(definition_tx.attributes)

    balances = wallet.balances_at(asset=asset)
    while balances['available_balance'] <= 0:
        print('\n...waiting for blockcypher testnet block...\n')
        time.sleep(5)
        balances = wallet.balances_at(asset=asset)

    print('\n\nwallet asset balance:\n')
    pprint(balances)

    new_addr = account.addresses.create()['string']

    transfer_tx = None

    while not transfer_tx:
        try:
            transfer_tx = asset.transfer(payees=[{'amount': 10, 'address': new_addr}], metadata=dict(some=dict(meta="data")))
            print('\n\nasset transfer:\n')
            pprint(transfer_tx.attributes)
        except:
            print('\n...waiting for blockcypher testnet block...\n')
            time.sleep(5)

    print('\n\n Entering interactive session.\n Interesting variables:\n  wallet, asset, account, addr, defintion_tx, new_addr, transfer_tx')
    pdb.set_trace()
