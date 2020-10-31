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
    drms.__version__.split('+')[0]
    m = re.match(r'(\d+)\.(\d+)\.(\d+).*', drms.__version__)
    assert m is not None


def test_bibtex():
    assert isinstance(drms.__citation__, str)
    m = re.match(r'.*Glogowski2019.*', drms.__citation__)
    assert m is not None
