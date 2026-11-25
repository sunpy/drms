from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

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


@pytest.mark.parametrize(
    ("process", "expected_proc_str"),
    [
        (None, "0"),
        ({}, "0"),
        ([], "0"),
        ({"im_patch": {"x": 0, "y": 0}}, "0|im_patch,x=0,y=0"),
        ({"aia_scale_aialev1": None}, "0|aia_scale_aialev1"),
        ({"aia_scale_aialev1": {}}, "0|aia_scale_aialev1"),
        ({"aia_scale_aialev1": {None: None}}, "0|aia_scale_aialev1"),
        (["aia_scale_aialev1"], "0|aia_scale_aialev1"),
        (("aia_scale_aialev1",), "0|aia_scale_aialev1"),
        ("aia_scale_aialev1", "0|aia_scale_aialev1"),
        (
            {"aia_scale_aialev1": {"mpt": "aia.master_pointing3h"}},
            "0|aia_scale_aialev1,mpt=aia.master_pointing3h",
        ),
        (
            [("aia_scale_aialev1", {"mpt": "aia.master_pointing3h"})],
            "0|aia_scale_aialev1,mpt=aia.master_pointing3h",
        ),
        (
            [{"aia_scale_aialev1": {"mpt": "aia.master_pointing3h"}}],
            "0|aia_scale_aialev1,mpt=aia.master_pointing3h",
        ),
        (
            ["aia_scale_aialev1", {"rebin": {"scale": 0.25}}],
            "0|aia_scale_aialev1|rebin,scale=0.25",
        ),
        (
            {"aia_scale_aialev1": None, "rebin": {"scale": 0.25}},
            "0|aia_scale_aialev1|rebin,scale=0.25",
        ),
    ],
)
def test_exp_request_url_process(process, expected_proc_str):
    c = Client()
    url = c._json._exp_request_url(
        "aia.lev1_euv_12s[2022-10-25T19:00][171]",
        "test@example.com",
        method="url",
        protocol="fits",
        process=process,
    )
    qs = parse_qs(urlparse(url).query)
    assert qs["process=n"] == [expected_proc_str]


def test_exp_request_url_process_invalid():
    c = Client()
    with pytest.raises(ValueError, match="foobar is not one of the allowed processing options"):
        c._json._exp_request_url(
            "aia.lev1_euv_12s[2022-10-25T19:00][171]",
            "test@example.com",
            method="url",
            protocol="fits",
            process={"foobar": {}},
        )

    for invalid_opt in (123, False, 0, [], "invalid"):
        with pytest.raises(TypeError, match="Processing options for 'im_patch' must be a dict or None"):
            c._json._exp_request_url(
                "aia.lev1_euv_12s[2022-10-25T19:00][171]",
                "test@example.com",
                method="url",
                protocol="fits",
                process={"im_patch": invalid_opt},
            )

    with pytest.raises(TypeError, match="process must be a dict, sequence, string, or None"):
        c._json._exp_request_url(
            "aia.lev1_euv_12s[2022-10-25T19:00][171]",
            "test@example.com",
            method="url",
            protocol="fits",
            process=123,
        )

    with pytest.raises(TypeError, match="Items in process sequence must be a string,"):
        c._json._exp_request_url(
            "aia.lev1_euv_12s[2022-10-25T19:00][171]",
            "test@example.com",
            method="url",
            protocol="fits",
            process=[123],
        )

    with pytest.raises(TypeError, match="Processing command name must be a string"):
        c._json._exp_request_url(
            "aia.lev1_euv_12s[2022-10-25T19:00][171]",
            "test@example.com",
            method="url",
            protocol="fits",
            process={(1, 2): None},
        )
