import re

import pytest

import drms


@pytest.mark.parametrize(
    'symbol',
    [
        'DrmsError',
        'DrmsQueryError',
        'DrmsExportError',
        'DrmsOperationNotSupported',
        'SeriesInfo',
        'ExportRequest',
        'Client',
        'const',
        'to_datetime',
    ],
)
def test_symbols(symbol):
    assert symbol in dir(drms)


def test_version():
    assert isinstance(drms.__version__, str)
    version = drms.__version__.split('+')[0]
    # Check to make sure it isn't empty
    assert version
    # To match the 0.6 in 0.6.dev3 or v0.6
    m = re.match(r'v*\d+\.\d+\.*', version)
    assert m is not None


def test_bibtex():
    assert isinstance(drms.__citation__, str)
    m = re.match(r'.*Glogowski2019.*', drms.__citation__)
    assert m is not None
