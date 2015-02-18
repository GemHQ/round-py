#DEFAULT_URL = u"https://api.gem.co"
#DEFAULT_NETWORK = u'bitcoin'

DEFAULT_URL = "https://api-sandbox.gem.co"
DEFAULT_NETWORK = u'testnet'

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
