from __future__ import absolute_import, division, print_function

import pytest
import drms


@pytest.mark.jsoc
@pytest.mark.parametrize('series, pkeys, segments', [
    ('hmi.v_45s', ['T_REC', 'CAMERA'], ['Dopplergram']),
    ('hmi.m_720s', ['T_REC', 'CAMERA'], ['magnetogram']),
    ('hmi.v_avg120', ['CarrRot', 'CMLon'], ['mean', 'power', 'valid', 'Log']),
    ])
def test_series_info_basic(jsoc_client, series, pkeys, segments):
    si = jsoc_client.info(series)
    assert si.name.lower() == series
    for k in pkeys:
        assert k in si.primekeys
        assert k in si.keywords.index
    for s in segments:
        assert s in si.segments.index
