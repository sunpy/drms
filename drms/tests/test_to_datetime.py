import numpy as np
import pandas as pd
import pytest

import drms

data_tai = [
    ('2010.05.01_TAI', pd.Timestamp('2010-05-01 00:00:00')),
    ('2010.05.01_00:00_TAI', pd.Timestamp('2010-05-01 00:00:00')),
    ('2010.05.01_00:00:00_TAI', pd.Timestamp('2010-05-01 00:00:00')),
    ('2010.05.01_01:23:45_TAI', pd.Timestamp('2010-05-01 01:23:45')),
    ('2013.12.21_23:32_TAI', pd.Timestamp('2013-12-21 23:32:00')),
    ('2013.12.21_23:32:34_TAI', pd.Timestamp('2013-12-21 23:32:34')),
]
data_tai_in = [data[0] for data in data_tai]
data_tai_out = pd.Series([data[1] for data in data_tai])


@pytest.mark.parametrize('time_string, expected', data_tai)
def test_tai_string(time_string, expected):
    assert drms.to_datetime(time_string) == expected


@pytest.mark.parametrize(
    'time_string, expected',
    [
        ('2010-05-01T00:00Z', pd.Timestamp('2010-05-01 00:00:00')),
        ('2010-05-01T00:00:00Z', pd.Timestamp('2010-05-01 00:00:00')),
        ('2010-05-01T01:23:45Z', pd.Timestamp('2010-05-01 01:23:45')),
        ('2013-12-21T23:32Z', pd.Timestamp('2013-12-21 23:32:00')),
        ('2013-12-21T23:32:34Z', pd.Timestamp('2013-12-21 23:32:34')),
        ('2010-05-01 00:00Z', pd.Timestamp('2010-05-01 00:00:00')),
        ('2010-05-01 00:00:00Z', pd.Timestamp('2010-05-01 00:00:00')),
        ('2010-05-01 01:23:45Z', pd.Timestamp('2010-05-01 01:23:45')),
        ('2013-12-21 23:32Z', pd.Timestamp('2013-12-21 23:32:00')),
        ('2013-12-21 23:32:34Z', pd.Timestamp('2013-12-21 23:32:34')),
    ],
)
def test_z_string(time_string, expected):
    assert drms.to_datetime(time_string) == expected


@pytest.mark.xfail(reason='pandas does not support leap seconds')
@pytest.mark.parametrize(
    'time_string, expected',
    [
        ('2012-06-30T23:59:60Z', '2012-06-30 23:59:60'),
        ('2015-06-30T23:59:60Z', '2015-06-30 23:59:60'),
        ('2016-12-31T23:59:60Z', '2016-12-31 23:59:60'),
    ],
)
def test_z_leap_string(time_string, expected):
    assert drms.to_datetime(time_string) == expected


@pytest.mark.parametrize(
    'time_string, expected',
    [
        ('2013.12.21_23:32:34_TAI', pd.Timestamp('2013-12-21 23:32:34')),
        ('2013.12.21_23:32:34_UTC', pd.Timestamp('2013-12-21 23:32:34')),
        ('2013.12.21_23:32:34Z', pd.Timestamp('2013-12-21 23:32:34')),
    ],
)
def test_force_string(time_string, expected):
    assert drms.to_datetime(time_string, force=True) == expected


@pytest.mark.parametrize(
    'time_series, expected',
    [
        (data_tai_in, data_tai_out),
        (pd.Series(data_tai_in), data_tai_out),
        (tuple(data_tai_in), data_tai_out),
        (np.array(data_tai_in), data_tai_out),
    ],
)
def test_time_series(time_series, expected):
    assert drms.to_datetime(time_series).equals(expected)


data_invalid = [
    ('2010.05.01_TAI', False),
    ('2010.05.01_00:00_TAI', False),
    ('', True),
    ('1600', True),
    ('foo', True),
    ('2013.12.21_23:32:34_TAI', False),
]
data_invalid_in = [data[0] for data in data_invalid]
data_invalid_out = pd.Series([data[1] for data in data_invalid])


@pytest.mark.parametrize('time_string, expected', data_invalid)
def test_corner_case(time_string, expected):
    assert pd.isnull(drms.to_datetime(time_string)) == expected
    assert isinstance(drms.to_datetime([]), pd.Series)
    assert drms.to_datetime([]).empty


@pytest.mark.parametrize(
    'time_series, expected',
    [
        (data_invalid_in, data_invalid_out),
        (pd.Series(data_invalid_in), data_invalid_out),
        (tuple(data_invalid_in), data_invalid_out),
        (np.array(data_invalid_in), data_invalid_out),
    ],
)
def test_corner_case_series(time_series, expected):
    assert pd.isnull(drms.to_datetime(time_series)).equals(expected)
