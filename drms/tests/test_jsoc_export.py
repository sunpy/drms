import pytest

import drms


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
@pytest.mark.parametrize('method', ['url_quick', 'url'])
def test_export_asis_basic(jsoc_client_export, method):
    r = jsoc_client_export.export(
        'hmi.v_avg120[2150]{mean,power}', protocol='as-is', method=method, requestor=False,
    )

    assert isinstance(r, drms.ExportRequest)
    assert r.wait(timeout=60)
    assert r.has_succeeded()
    assert r.protocol == 'as-is'
    assert len(r.urls) == 12  # 6 files per segment

    for record in r.urls.record:
        record = record.lower()
        assert record.startswith('hmi.v_avg120[2150]')
        assert record.endswith('{mean}') or record.endswith('{power}')

    for filename in r.urls.filename:
        assert filename.endswith('mean.fits') or filename.endswith('power.fits')

    for url in r.urls.url:
        assert url.endswith('mean.fits') or url.endswith('power.fits')


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_export_fits_basic(jsoc_client_export):
    r = jsoc_client_export.export(
        'hmi.sharp_720s[4864][2014.11.30_00:00_TAI]{continuum, magnetogram}',
        protocol='fits',
        method='url',
        requestor=False,
    )

    assert isinstance(r, drms.ExportRequest)
    assert r.wait(timeout=60)
    assert r.has_succeeded()
    assert r.protocol == 'fits'
    assert len(r.urls) == 2  # 1 file per segment

    for record in r.urls.record:
        record = record.lower()
        assert record.startswith('hmi.sharp_720s[4864]')
        assert record.endswith('2014.11.30_00:00:00_tai]')

    for filename in r.urls.filename:
        assert filename.endswith('continuum.fits') or filename.endswith('magnetogram.fits')

    for url in r.urls.url:
        assert url.endswith('continuum.fits') or url.endswith('magnetogram.fits')


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_export_email(jsoc_client):
    with pytest.raises(ValueError):
        jsoc_client.export('hmi.v_45s[2016.04.01_TAI/1d@6h]{Dopplergram}')
