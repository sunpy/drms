from __future__ import absolute_import, division, print_function

import pytest
import drms


@pytest.mark.jsoc
def test_query_basic(jsoc_client):
    keys, segs = jsoc_client.query(
        'hmi.v_45s[2013.07.03_08:42_TAI/3m]',
        key='T_REC, CRLT_OBS', seg='Dopplergram')
    assert len(keys) == 4
    for k in ['T_REC', 'CRLT_OBS']:
        assert k in keys.columns
    assert len(segs) == 4
    assert 'Dopplergram' in segs.columns
    assert ((keys.CRLT_OBS - 3.14159).abs() < 0.0001).all()
