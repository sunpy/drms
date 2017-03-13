from __future__ import absolute_import, division, print_function

import pytest
import six
import re
import drms


@pytest.mark.parametrize('symbol', [
    'DrmsError', 'DrmsQueryError', 'DrmsExportError',
    'DrmsOperationNotSupported',
    'SeriesInfo', 'ExportRequest', 'Client',
    'const', 'to_datetime',
    ])
def test_symbols(symbol):
    assert symbol in dir(drms)


def test_version():
    assert isinstance(drms.__version__, six.string_types)
    vstr = drms.__version__.split('+')[0]
    m = re.match(r'(\d+)\.(\d+)\.(\d+).*', drms.__version__)
    assert m is not None
