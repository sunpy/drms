from __future__ import absolute_import, division, print_function

import re
import six
import pandas as pd

from drms.utils import _extract_series_name, _split_arg

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
