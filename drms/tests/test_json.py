import pytest

from drms.client import Client
from drms.json import JsocInfoConstants


@pytest.mark.remote_data()
def test_jsocinfoconstants():
    assert isinstance(JsocInfoConstants.all, str)
    assert JsocInfoConstants.all == "**ALL**"
    client = Client()
    client.query("hmi.synoptic_mr_720s[2150]", key=JsocInfoConstants.all, seg="synopMr")
