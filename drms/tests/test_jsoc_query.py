import pytest

import drms
from drms.config import ServerConfig
from drms.exceptions import DrmsOperationNotSupported, DrmsQueryError


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_basic(jsoc_client):
    keys, segs = jsoc_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', key='T_REC, CRLT_OBS', seg='Dopplergram')
    assert len(keys) == 4
    for k in ['T_REC', 'CRLT_OBS']:
        assert k in keys.columns
    assert len(segs) == 4
    assert 'Dopplergram' in segs.columns
    assert ((keys.CRLT_OBS - 3.14159).abs() < 0.0001).all()


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_allmissing(jsoc_client):
    with pytest.raises(ValueError):
        keys = jsoc_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]')


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_key(jsoc_client):
    keys = jsoc_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', key='T_REC, CRLT_OBS')
    assert len(keys) == 4
    for k in ['T_REC', 'CRLT_OBS']:
        assert k in keys.columns
    assert ((keys.CRLT_OBS - 3.14159).abs() < 0.0001).all()


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_seg(jsoc_client):
    segs = jsoc_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', seg='Dopplergram')
    assert len(segs) == 4
    assert 'Dopplergram' in segs.columns


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_link(jsoc_client):
    links = jsoc_client.query('hmi.B_720s[2013.07.03_08:42_TAI/40m]', link='MDATA')
    assert len(links) == 3
    assert 'MDATA' in links.columns


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_seg_key_link(jsoc_client):
    keys, segs, links = jsoc_client.query('hmi.B_720s[2013.07.03_08:42_TAI/40m]', key='foo', link='bar', seg='baz')
    assert len(keys) == 3
    assert (keys.foo == 'Invalid KeyLink').all()
    assert len(segs) == 3
    assert (segs.baz == 'InvalidSegName').all()
    assert len(links) == 3
    assert (links.bar == 'Invalid_Link').all()


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_pkeys(jsoc_client):
    keys = jsoc_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', pkeys=True)
    pkeys = list(keys.columns.values)
    assert pkeys == jsoc_client.pkeys('hmi.v_45s[2013.07.03_08:42_TAI/3m]')
    assert len(keys) == 4


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_recindex(jsoc_client):
    keys = jsoc_client.query('hmi.V_45s[2013.07.03_08:42_TAI/4m]', key='T_REC', rec_index=True)
    index_values = list(keys.index.values)
    assert all(['hmi.V_45s' in s for s in index_values])
    assert len(keys) == 5


def test_query_invalid_server():
    cfg = ServerConfig(name='TEST')
    c = drms.Client(server=cfg)
    with pytest.raises(DrmsOperationNotSupported):
        keys = c.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', pkeys=True)


@pytest.mark.jsoc
@pytest.mark.remote_data
def test_query_invalid_series(jsoc_client):
    with pytest.raises(DrmsQueryError):
        keys = jsoc_client.query('foo', key='T_REC')
