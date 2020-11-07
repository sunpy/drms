import pytest

import drms
from drms.config import ServerConfig


def test_client_init_defaults():
    c = drms.Client()
    assert isinstance(c._server, ServerConfig)
    assert c._server.name.lower() == 'jsoc'
    assert c.email is None
    assert c.verbose is False
    assert c.debug is False


@pytest.mark.parametrize('value', [True, False])
def test_client_init_verbose(value):
    c = drms.Client(verbose=value)
    assert c.verbose is value
    assert c.debug is False


@pytest.mark.parametrize('value', [True, False])
def test_client_init_debug(value):
    c = drms.Client(debug=value)
    assert c.verbose is False
    assert c.debug is value


@pytest.mark.parametrize('server_name', ['jsoc', 'kis'])
def test_client_registered_servers(server_name):
    c = drms.Client(server_name)
    assert isinstance(c._server, ServerConfig)
    assert c._server.name.lower() == server_name
    assert c.email is None
    assert c.verbose is False
    assert c.debug is False


def test_client_custom_config():
    cfg = ServerConfig(name='TEST')
    c = drms.Client(server=cfg)
    assert isinstance(c._server, ServerConfig)
    assert c._server.name == 'TEST'


def test_repr():
    assert repr(drms.Client()) == '<Client: JSOC>'
    assert repr(drms.Client(server='kis')) == '<Client: KIS>'
