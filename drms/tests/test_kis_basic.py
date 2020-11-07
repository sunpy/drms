import pytest

import drms


@pytest.mark.kis
@pytest.mark.remote_data
def test_series_list_all(kis_client):
    slist = kis_client.series()
    assert isinstance(slist, list)
    assert 'hmi.v_45s' in (s.lower() for s in slist)
    assert 'hmi.m_720s' in (s.lower() for s in slist)
    assert 'hmi.ic_720s' in (s.lower() for s in slist)
    assert 'mdi.fd_v' in (s.lower() for s in slist)


@pytest.mark.kis
@pytest.mark.remote_data
@pytest.mark.parametrize('schema', ['hmi', 'mdi'])
def test_series_list_schemata(kis_client, schema):
    regex = fr'{schema}\.'
    slist = kis_client.series(regex)
    assert len(slist) > 0
    for sname in slist:
        assert sname.startswith(f'{schema}.')


@pytest.mark.kis
@pytest.mark.remote_data
@pytest.mark.parametrize(
    'series, pkeys, segments',
    [
        ('hmi.v_45s', ['T_REC', 'CAMERA'], ['Dopplergram']),
        ('hmi.m_720s', ['T_REC', 'CAMERA'], ['magnetogram']),
        ('hmi.v_avg120', ['CarrRot', 'CMLon'], ['mean', 'power', 'valid', 'Log']),
    ],
)
def test_series_info_basic(kis_client, series, pkeys, segments):
    si = kis_client.info(series)
    assert si.name.lower() == series
    for k in pkeys:
        assert k in si.primekeys
        assert k in si.keywords.index
    for s in segments:
        assert s in si.segments.index


@pytest.mark.kis
@pytest.mark.remote_data
def test_query_basic(kis_client):
    keys, segs = kis_client.query('hmi.v_45s[2013.07.03_08:42_TAI/3m]', key='T_REC, CRLT_OBS', seg='Dopplergram')
    assert len(keys) == 4
    for k in ['T_REC', 'CRLT_OBS']:
        assert k in keys.columns
    assert len(segs) == 4
    assert 'Dopplergram' in segs.columns
    assert ((keys.CRLT_OBS - 3.14159).abs() < 0.0001).all()


@pytest.mark.kis
@pytest.mark.remote_data
def test_not_supported_email(kis_client):
    with pytest.raises(drms.DrmsOperationNotSupported):
        kis_client.email = 'name@example.com'


@pytest.mark.kis
@pytest.mark.remote_data
def test_not_supported_export(kis_client):
    with pytest.raises(drms.DrmsOperationNotSupported):
        kis_client.export('hmi.v_45s[2010.05.01_TAI]')
    with pytest.raises(drms.DrmsOperationNotSupported):
        kis_client.export_from_id('KIS_20120101_123')
