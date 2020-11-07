import pytest


@pytest.mark.jsoc
@pytest.mark.remote_data
@pytest.mark.parametrize(
    'series, pkeys, segments',
    [
        ('hmi.v_45s', ['T_REC', 'CAMERA'], ['Dopplergram']),
        ('hmi.m_720s', ['T_REC', 'CAMERA'], ['magnetogram']),
        ('hmi.v_avg120', ['CarrRot', 'CMLon'], ['mean', 'power', 'valid', 'Log']),
    ],
)
def test_series_info_basic(jsoc_client, series, pkeys, segments):
    si = jsoc_client.info(series)
    assert si.name.lower() == series
    for k in pkeys:
        assert k in si.primekeys
        assert k in si.keywords.index
    for s in segments:
        assert s in si.segments.index


@pytest.mark.jsoc
@pytest.mark.remote_data
@pytest.mark.parametrize(
    'series, pkeys',
    [
        ('hmi.v_45s', ['T_REC', 'CAMERA']),
        ('hmi.m_720s', ['T_REC', 'CAMERA']),
        ('hmi.v_avg120', ['CarrRot', 'CMLon']),
        ('aia.lev1', ['T_REC', 'FSN']),
        ('aia.lev1_euv_12s', ['T_REC', 'WAVELNTH']),
        ('aia.response', ['T_START', 'WAVE_STR']),
        ('iris.lev1', ['T_OBS', 'FSN']),
        ('mdi.fd_m_lev182', ['T_REC']),
    ],
)
def test_series_primekeys(jsoc_client, series, pkeys):
    pkey_list = jsoc_client.pkeys(series)
    key_list = jsoc_client.keys(series)
    for k in pkeys:
        assert k in pkey_list
        assert k in key_list
