from __future__ import absolute_import, division, print_function

import pytest
from six.moves.urllib.request import urlopen
from six.moves.urllib.error import URLError, HTTPError
import drms


# Directory containing all online tests
online_tests_dir = 'online'

# Filename prefixes for JSOC and KIS online tests
jsoc_tests_prefix = 'test_jsoc'
kis_tests_prefix = 'test_kis'

# Test URLs, used to check if a online site is reachable
jsoc_testurl = 'http://jsoc.stanford.edu/'
kis_testurl = 'http://drms.leibniz-kis.de/'


def pytest_configure(config):
    # Register markers here so we don't need to add a pytest.ini file to
    # the drms.tests subpackage.
    config.addinivalue_line(
        'markers', 'jsoc: mark online tests for JSOC')
    config.addinivalue_line(
        'markers', 'kis: mark online tests for KIS')
    config.addinivalue_line(
        'markers', 'export: mark online tests that perform data exports')


def pytest_addoption(parser):
    # Add command line options for enabling online tests
    parser.addoption('--run-jsoc', action='store_true',
                     help='Run online tests for JSOC')
    parser.addoption('--run-kis', action='store_true',
                     help='Run online tests for KIS')
    parser.addoption('--email', help='Export email address')


def pytest_ignore_collect(path, config):
    # Handle selection of site-specific online tests.
    if path.dirname.endswith(online_tests_dir) and path.ext == '.py':
        # Only run online tests for JSOC, if --run-jsoc is specified.
        if not config.getoption('run_jsoc'):
            if path.basename.startswith(jsoc_tests_prefix):
                return True

        # Only run online tests for KIS, if --run-kis is specified.
        if not config.getoption('run_kis'):
            if path.basename.startswith(kis_tests_prefix):
                return True

    return False


class lazily_cached(object):
    """Lazily evaluted function call with cached result."""
    def __init__(self, f, *args, **kwargs):
        self.func = lambda: f(*args, **kwargs)

    def __call__(self):
        if not hasattr(self, 'result'):
            self.result = self.func()
        return self.result


def site_reachable(url, timeout=3):
    """Checks if the given URL is accessible."""
    try:
        urlopen(url, timeout=timeout)
    except (URLError, HTTPError):
        return False
    return True


# Create lazily evaluated, cached site checks for JSOC and KIS.
jsoc_reachable = lazily_cached(site_reachable, jsoc_testurl)
kis_reachable = lazily_cached(site_reachable, kis_testurl)


def _get_item_marker(item, name):
    """
    Compatibility function for pytest < 3.6.

    Notes
    -----
    The method pytest.Item.get_closest_marker() is available since pytest 3.6,
    while the method pytest.Item.get_marker() was removed in pytest 4.1.
    """
    if hasattr(item, 'get_closest_marker'):
        return item.get_closest_marker(name)
    else:
        return item.get_marker(name)


def pytest_runtest_setup(item):
    # Skip JSOC online site tests if the site is not reachable.
    if _get_item_marker(item, 'jsoc') is not None:
        if not jsoc_reachable():
            pytest.skip('JSOC is not reachable')

    # Skip KIS online site tests if the site is not reachable.
    if _get_item_marker(item, 'kis') is not None:
        if not kis_reachable():
            pytest.skip('KIS is not reachable')

    # Skip export tests if no email address was specified.
    if _get_item_marker(item, 'export') is not None:
        email = item.config.getoption('email')
        if email is None:
            pytest.skip('No email address specified; use the --email '
                        'option to enable export tests')


@pytest.fixture
def email(request):
    """Email address from --email command line option."""
    return request.config.getoption('--email')


@pytest.fixture
def jsoc_client():
    """Client fixture for JSOC online tests, does not use email."""
    return drms.Client('jsoc')


@pytest.fixture
def jsoc_client_export(email):
    """Client fixture for JSOC online tests, uses email if specified."""
    return drms.Client('jsoc', email=email)


@pytest.fixture
def kis_client():
    """Client fixture for KIS online tests."""
    return drms.Client('kis')
