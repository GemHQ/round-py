DEFAULT_ENVIRONMENT = u'sandbox'

ENV_MAP = {u'sandbox': {u'network': u'testnet',
                        u'url': u'https://api-sandbox.gem.co'},
           u'production': {u'network': u'bitcoin',
                           u'url': u'https://api.gem.co'}}

SUPPORTED_NETWORKS = [u'testnet', u'bitcoin']

NETWORK_MAP = {u'testnet': u'testnet',
               u'testnet3': u'testnet',
               u'bitcoin_testnet': u'testnet',
               u'mainnet': u'mainnet',
               u'bitcoin': u'mainnet',
               u'bitcoin_mainnet': u'mainnet'}

GEM_NETWORK = {u'mainnet': u'bitcoin',
               u'bitcoin': u'bitcoin',
               u'bitcoin_mainnet': u'bitcoin',
               u'testnet': u'bitcoin_testnet',
               u'testnet3': u'bitcoin_testnet',
               u'bitcoin_testnet': u'bitcoin_testnet'}
