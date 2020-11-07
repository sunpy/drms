from urllib.error import URLError, HTTPError
from urllib.request import urlopen

import pytest

import drms

# Test URLs, used to check if a online site is reachable
jsoc_testurl = 'http://jsoc.stanford.edu/'
kis_testurl = 'http://drms.leibniz-kis.de/'


def pytest_addoption(parser):
    parser.addoption('--email', help='Export email address')


class lazily_cached:
    """
    Lazily evaluted function call with cached result.
    """

    def __init__(self, f, *args, **kwargs):
        self.func = lambda: f(*args, **kwargs)

    def __call__(self):
        if not hasattr(self, 'result'):
            self.result = self.func()
        return self.result


def site_reachable(url, timeout=15):
    """
    Checks if the given URL is accessible.
    """
    try:
        urlopen(url, timeout=timeout)
    except (URLError, HTTPError):
        return False
    return True


# Create lazily evaluated, cached site checks for JSOC and KIS.
jsoc_reachable = lazily_cached(site_reachable, jsoc_testurl)
kis_reachable = lazily_cached(site_reachable, kis_testurl)


def pytest_runtest_setup(item):
    # Skip JSOC online site tests if the site is not reachable.
    if item.get_closest_marker('jsoc') is not None:
        if not jsoc_reachable():
            pytest.skip('JSOC is not reachable')

    # Skip KIS online site tests if the site is not reachable.
    if item.get_closest_marker('kis') is not None:
        if not kis_reachable():
            pytest.skip('KIS is not reachable')

    # Skip export tests if no email address was specified.
    if item.get_closest_marker('export') is not None:
        email = item.config.getoption('email')
        if email is None:
            pytest.skip('No email address specified; use the --email option to enable export tests')


@pytest.fixture
def email(request):
    """
    Email address from --email command line option.
    """
    return request.config.getoption('--email')


@pytest.fixture
def jsoc_client():
    """
    Client fixture for JSOC online tests, does not use email.
    """
    return drms.Client('jsoc')


@pytest.fixture
def jsoc_client_export(email):
    """
    Client fixture for JSOC online tests, uses email if specified.
    """
    return drms.Client('jsoc', email=email)


@pytest.fixture
def kis_client():
    """
    Client fixture for KIS online tests.
    """
    return drms.Client('kis')
