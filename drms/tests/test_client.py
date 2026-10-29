import drms
from drms.config import ServerConfig

from unittest.mock import MagicMock
import pytest



def test_client_init_defaults():
    c = drms.Client()
    assert isinstance(c._server, ServerConfig)
    assert c._server.name.lower() == "jsoc"
    assert c.email is None


@pytest.mark.parametrize("server_name", ["jsoc", "kis"])
def test_client_registered_servers(server_name):
    c = drms.Client(server_name)
    assert isinstance(c._server, ServerConfig)
    assert c._server.name.lower() == server_name
    assert c.email is None


def test_client_custom_config():
    cfg = ServerConfig(name="TEST")
    c = drms.Client(cfg)
    assert isinstance(c._server, ServerConfig)
    assert c._server.name == "TEST"


def test_repr():
    assert repr(drms.Client()) == "<Client: JSOC>"
    assert repr(drms.Client("kis")) == "<Client: KIS>"


def test_export_request_status_update():
    mock_client = MagicMock()
    mock_client._json.exp_status.return_value = {"status": 0, "requestid": "EXP_123"}

    # initialize with pending statsu
    req = drms.ExportRequest({"status": 2, "requestid": "EXP_123"}, client=mock_client)
    assert req._status == 2

    assert req.status == 0
    mock_client._json.exp_status.assert_called_once_with("EXP_123")

    mock_client.reset_mock()
    assert req.status == 0
    mock_client._json.exp_status.assert_not_called()
