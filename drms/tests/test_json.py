from unittest.mock import patch

import pytest

from drms.client import Client
from drms.json import HttpJsonRequest, JsocInfoConstants


@pytest.mark.remote_data()
def test_jsocinfoconstants():
    assert isinstance(JsocInfoConstants.all, str)
    assert JsocInfoConstants.all == "**ALL**"
    client = Client()
    client.query("hmi.synoptic_mr_720s[2150]", key=JsocInfoConstants.all, seg="synopMr")


def test_request_headers():
    with patch("drms.json.urlopen") as mock:
        HttpJsonRequest("http://example.com", "latin1")

    actual_request = mock.call_args[0][0]
    assert actual_request.headers["User-agent"]
    assert "drms/" in actual_request.headers["User-agent"]
    assert "python/" in actual_request.headers["User-agent"]
    assert actual_request.full_url == "http://example.com"
