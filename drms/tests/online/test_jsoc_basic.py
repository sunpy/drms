from __future__ import absolute_import, division, print_function

import pytest
import drms


@pytest.mark.jsoc
def test_series_list_all(jsoc_client):
    slist = jsoc_client.series()
    assert isinstance(slist, list)
    assert 'hmi.v_45s' in (s.lower() for s in slist)
    assert 'hmi.m_720s' in (s.lower() for s in slist)
    assert 'hmi.ic_720s' in (s.lower() for s in slist)
    assert 'aia.lev1' in (s.lower() for s in slist)
    assert 'aia.lev1_euv_12s' in (s.lower() for s in slist)
    assert 'mdi.fd_v' in (s.lower() for s in slist)


@pytest.mark.jsoc
@pytest.mark.parametrize('schema', ['aia', 'hmi', 'mdi'])
def test_series_list_schemata(jsoc_client, schema):
    regex = r'%s\.' % schema
    slist = jsoc_client.series(regex)
    assert len(slist) > 0
    for sname in slist:
        assert sname.startswith(schema + '.')
