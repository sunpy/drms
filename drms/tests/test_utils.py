from __future__ import absolute_import, division, print_function

import re
import six
import pandas as pd
import numpy

from drms.utils import _extract_series_name, _split_arg, to_datetime, _pd_to_datetime_coerce, _pd_to_numeric_coerce

def test_extract_series_name():

	ds1 = 'hmi.v_45s[2016.04.01_TAI/1d@6h]{Dopplergram}'
	exp_sn = 'hmi.v_45s'
	assert _extract_series_name(ds1) == exp_sn

def test_extract_series_name_corner():

	ds1 = '[2016.04.01_TAI/1d@6h]'
	ds2 = '{Dopplergram}'
	exp_sn = None
	assert _extract_series_name(ds1) == None
	assert _extract_series_name(ds2) == None

def test_split_arg():

	arg = 'foo,bar,baz'
	exp = ['foo','bar','baz']
	assert _split_arg(arg) == exp

def test_pd_to_numeric_coerce():

	arg1 = pd.Series(['1.0', '2', -3])
	arg2 = pd.Series(['1.0', 'apple', -3])
	exp1 = pd.Series([1.0, 2.0, -3.0])
	exp2 = pd.Series([1.0, float('nan'), -3.0])

	assert _pd_to_numeric_coerce(arg1).equals(exp1)
	assert _pd_to_numeric_coerce(arg2).equals(exp2)

def test_pd_to_datetime_coerce():

	arg = pd.Series(['2016-04-01 00:00:00','2016-04-01 06:00:00','2016-04-01 12:00:00'])
	exp = pd.Series([pd.Timestamp('2016-04-01 00:00:00'),pd.Timestamp('2016-04-01 06:00:00'),
		             pd.Timestamp('2016-04-01 12:00:00')])
	assert _pd_to_datetime_coerce(arg).equals(exp)

def test_to_datetime_series():

	tstr = pd.Series(['2016.04.01_00:00:00_TAI','2016.04.01_06:00:00_TAI','2016.04.01_12:00:00_TAI'])
	exp = pd.Series([pd.Timestamp('2016-04-01 00:00:00'),pd.Timestamp('2016-04-01 06:00:00'),
		             pd.Timestamp('2016-04-01 12:00:00')])

	assert isinstance(to_datetime(tstr), pd.Series)
	assert to_datetime(tstr).equals(exp)

def test_to_datetime_str():
	
	tstr = '2016.04.01_00:00:00_TAI'
	exp = pd.Timestamp('2016-04-01 00:00:00')
	assert isinstance(to_datetime(tstr), pd.Timestamp)
	assert to_datetime(tstr) == exp