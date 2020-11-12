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
def test_export_im_patch(jsoc_client_export):
    # TODO: check that this has actually done the export/processing properly?
    # NOTE: processing exports seem to fail silently on the server side if
    # the correct names/arguments are not passed. Not clear how to check
    # that this has not happened.
    process = {'im_patch': {
        't_ref': '2015-10-17T04:33:30.000',
        't': 0,
        'r': 0,
        'c': 0,
        'locunits': 'arcsec',
        'boxunits': 'arcsec',
        'x': -517.2,
        'y': -246,
        'width': 345.6,
        'height': 345.6,
    }}
    req = jsoc_client_export.export(
        'aia.lev1_euv_12s[2015-10-17T04:33:30.000/1m@12s][171]{image}',
        method='url',
        protocol='fits',
        process=process,
        requestor=False,
    )

    assert isinstance(req, drms.ExportRequest)
    assert req.wait(timeout=60)
    assert req.has_succeeded()
    assert req.protocol == 'fits'

    for record in req.urls.record:
        record = record.lower()
        assert record.startswith('aia.lev1_euv_12s_mod')

    for filename in req.urls.filename:
        assert filename.endswith('image.fits')

    for url in req.urls.url:
        assert url.endswith('image.fits')


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_export_rebin(jsoc_client_export):
    # TODO: check that this has actually done the export/processing properly?
    # NOTE: processing exports seem to fail silently on the server side if
    # the correct names/arguments are not passed. Not clear how to check
    # that this has not happened.
    req = jsoc_client_export.export(
        'hmi.M_720s[2020-10-17_22:12:00_TAI/24m]{magnetogram}',
        method='url',
        protocol='fits',
        process={'rebin': {'method': 'boxcar', 'scale': 0.25}},
        requestor=False,
    )

    assert isinstance(req, drms.ExportRequest)
    assert req.wait(timeout=60)
    assert req.has_succeeded()
    assert req.protocol == 'fits'

    for record in req.urls.record:
        record = record.lower()
        assert record.startswith('hmi.m_720s_mod')

    for filename in req.urls.filename:
        assert filename.endswith('magnetogram.fits')

    for url in req.urls.url:
        assert url.endswith('magnetogram.fits')


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_export_invalid_process(jsoc_client_export):
    with pytest.raises(ValueError, match='foobar is not one of the allowed processing options'):
        jsoc_client_export.export(
            'aia.lev1_euv_12s[2015-10-17T04:33:30.000/1m@12s][171]{image}',
            process={'foobar': {}}
        )


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_export_email(jsoc_client):
    with pytest.raises(ValueError):
        jsoc_client.export('hmi.v_45s[2016.04.01_TAI/1d@6h]{Dopplergram}')
