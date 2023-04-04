import re

import pytest

import drms


@pytest.mark.parametrize(
    "symbol",
    [
        "__bibtex__",
        "__citation__",
        "__version__",
        "client",
        "Client",
        "config",
        "DrmsError",
        "DrmsExportError",
        "DrmsOperationNotSupported",
        "DrmsQueryError",
        "exceptions",
        "ExportRequest",
        "HttpJsonClient",
        "HttpJsonRequest",
        "JsocInfoConstants",
        "json",
        "main",
        "Path",
        "register_server",
        "SeriesInfo",
        "ServerConfig",
        "to_datetime",
        "utils",
        "version",
    ],
)
def test_symbols(symbol):
    assert symbol in dir(drms)


def test_version():
    assert isinstance(drms.__version__, str)
    version = drms.__version__.split("+")[0]
    # Check to make sure it isn't empty
    assert version
    # To match the 0.6 in 0.6.dev3 or v0.6
    m = re.match(r"v*\d+\.\d+\.*", version)
    assert m is not None


def test_bibtex():
    assert isinstance(drms.__citation__, str)
    m = re.match(r".*Glogowski2019.*", drms.__citation__)
    assert m is not None
