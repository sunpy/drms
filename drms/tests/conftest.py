import os
from urllib.error import URLError, HTTPError
from urllib.request import urlopen

import pytest

from drms.utils import create_request_with_header

# Test URLs, used to check if a online site is reachable
jsoc_testurl = "http://jsoc.stanford.edu/"
kis_testurl = "http://drms.leibniz-kis.de/"


class lazily_cached:
    """
    Lazily evaluated function call with cached result.
    """

    def __init__(self, f, *args, **kwargs):
        self.func = lambda: f(*args, **kwargs)

    def __call__(self):
        if not hasattr(self, "result"):
            self.result = self.func()
        return self.result


def site_reachable(url, timeout=60):
    """
    Checks if the given URL is accessible.
    """
    try:
        urlopen(create_request_with_header(url), timeout=timeout)
    except (URLError, HTTPError):
        return False
    return True


# Create lazily evaluated, cached site checks for JSOC and KIS.
jsoc_reachable = lazily_cached(site_reachable, jsoc_testurl)
kis_reachable = lazily_cached(site_reachable, kis_testurl)


def pytest_runtest_setup(item):
    # Skip JSOC online site tests if the site is not reachable.
    if item.get_closest_marker("jsoc") is not None:
        if not jsoc_reachable():
            pytest.skip("JSOC is not reachable")

    # Skip KIS online site tests if the site is not reachable.
    if item.get_closest_marker("kis") is not None:
        if not kis_reachable():
            pytest.skip("KIS is not reachable")


@pytest.fixture()
def email():
    """
    Email address for tests.
    """
    email = os.environ.get("JSOC_EMAIL", None)
    if email is None:
        pytest.skip("No email address specified; use the JSOC_EMAIL environmental variable to enable export tests")
    return email


@pytest.fixture()
def jsoc_client():
    """
    Client fixture for JSOC online tests, does not use email.
    """
    import drms

    return drms.Client("jsoc")


@pytest.fixture()
def jsoc_client_export(email):
    """
    Client fixture for JSOC online tests, uses email if specified.
    """
    import drms

    return drms.Client("jsoc", email=email)


@pytest.fixture()
def kis_client():
    """
    Client fixture for KIS online tests.
    """
    import drms

    return drms.Client("kis")
