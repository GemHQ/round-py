# -*- coding: utf-8 -*-
import pytest

def pytest_addoption(parser):
    parser.addoption("--host", action="store", default='https://api-develop.gem.co', help="specify the url of test host (optional) default: https://api-develop.gem.co (scheme is optional and defaults to http)")
    parser.addoption("--port", action="store", default='443', help="specify the port of test host (optional) default: 443")

@pytest.fixture(scope=u'session')
def api_url(request):
    url = "{}:{}".format(request.config.getoption('--host'),
                         request.config.getoption('--port'))
    return u'http://' + url if u'://' not in url else url
