from __future__ import absolute_import, division, print_function

import pytest
from drms.utils import (
    _pd_to_datetime_coerce, _pd_to_numeric_coerce,
    _split_arg, _extract_series_name)


# test_pd_to_datetime
# test_pd_to_numeric


@pytest.mark.parametrize('in_obj, expected', [
    ('', []),
    ('asd', ['asd']),
    ('aa,bb,cc', ['aa', 'bb', 'cc']),
    ('aa, bb, cc', ['aa', 'bb', 'cc']),
    (' aa,bb,  cc, dd', ['aa', 'bb', 'cc', 'dd']),
    ('aa,\tbb,cc, dd ', ['aa', 'bb', 'cc', 'dd']),
    (u'aa,\tbb,cc, dd ', [u'aa', u'bb', u'cc', u'dd']),
    ([], []),
    (['a', 'b', 'c'], ['a', 'b', 'c']),
    (('a', 'b', 'c'), ['a', 'b', 'c']),
    ])
def test_split_arg(in_obj, expected):
    res = _split_arg(in_obj)
    assert len(res) == len(expected)
    for i in range(len(res)):
        assert res[i] == expected[i]


@pytest.mark.parametrize('ds_string, expected', [
    ('hmi.v_45s', 'hmi.v_45s'),
    ('hmi.v_45s[2010.05.01_TAI]', 'hmi.v_45s'),
    ('hmi.v_45s[2010.05.01_TAI/365d@1d]', 'hmi.v_45s'),
    ('hmi.v_45s[2010.05.01_TAI/365d@1d][?QUALITY>=0?]', 'hmi.v_45s'),
    ('hmi.v_45s[2010.05.01_TAI/1d@6h]{Dopplergram}', 'hmi.v_45s'),
    ])
def test_extract_series(ds_string, expected):
    assert _extract_series_name(ds_string) == expected
