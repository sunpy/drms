import pytest

import drms


@pytest.mark.jsoc()
@pytest.mark.remote_data()
@pytest.mark.parametrize("method", ["url_quick", "url"])
def test_export_asis_basic(jsoc_client_export, method):
    r = jsoc_client_export.export(
        "hmi.v_sht_2drls[2024.09.19_00:00:00_TAI]{split,rot,err}",
        protocol="as-is",
        method=method,
        requester=False,
    )

    assert isinstance(r, drms.ExportRequest)
    assert r.wait(timeout=60)
    assert r.has_succeeded()
    assert r.protocol == "as-is"
    assert len(r.urls) == 9  # 3 files per segment

    for record in r.urls.record:
        record = record.lower()
        assert record.startswith("hmi.v_sht_2drls[2024.09.19_00:00:00_tai]")
        assert record.endswith(("{split}", "{rot}", "{err}"))

    for filename in r.urls.filename:
        assert filename.endswith(("err.2d", "rot.2d", "splittings.out"))

    for url in r.urls.url:
        assert url.endswith(("err.2d", "rot.2d", "splittings.out"))


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_export_fits_basic(jsoc_client_export):
    r = jsoc_client_export.export(
        "hmi.sharp_720s[4864][2014.11.30_00:00_TAI]{continuum, magnetogram}",
        protocol="fits",
        method="url",
        requester=False,
    )

    assert isinstance(r, drms.ExportRequest)
    assert r.wait(timeout=60)
    assert r.has_succeeded()
    assert r.protocol == "fits"
    assert len(r.urls) == 2  # 1 file per segment

    for record in r.urls.record:
        record = record.lower()
        assert record.startswith("hmi.sharp_720s[4864]")
        assert record.endswith("2014.11.30_00:00:00_tai]")

    for filename in r.urls.filename:
        assert filename.endswith(("continuum.fits", "magnetogram.fits"))

    for url in r.urls.url:
        assert url.endswith(("continuum.fits", "magnetogram.fits"))


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_export_im_patch(jsoc_client_export):
    # TODO: check that this has actually done the export/processing properly?
    # NOTE: processing exports seem to fail silently on the server side if
    # the correct names/arguments are not passed. Not clear how to check
    # that this has not happened.
    process = {
        "im_patch": {
            "t_ref": "2025-01-01T04:33:30.000",
            "t": 0,
            "r": 0,
            "c": 0,
            "locunits": "arcsec",
            "boxunits": "arcsec",
            "x": -517.2,
            "y": -246,
            "width": 345.6,
            "height": 345.6,
        },
    }
    req = jsoc_client_export.export(
        "aia.lev1_euv_12s[2025-01-01T04:33:30.000/1m@12s][171]{image}",
        method="url",
        protocol="fits",
        process=process,
        requester=False,
    )

    assert isinstance(req, drms.ExportRequest)
    assert req.wait(timeout=60)
    assert req.has_succeeded()
    assert req.protocol == "fits"

    for record in req.urls.record:
        record = record.lower()
        assert record.startswith("aia.lev1_euv_12s_mod")

    for filename in req.urls.filename:
        assert filename.endswith("image.fits")

    for url in req.urls.url:
        assert url.endswith("image.fits")


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_export_rebin(jsoc_client_export):
    # TODO: check that this has actually done the export/processing properly?
    # NOTE: processing exports seem to fail silently on the server side if
    # the correct names/arguments are not passed. Not clear how to check
    # that this has not happened.
    req = jsoc_client_export.export(
        "hmi.M_720s[2020-10-17_22:12:00_TAI/24m]{magnetogram}",
        method="url",
        protocol="fits",
        process={"rebin": {"method": "boxcar", "scale": 0.25}},
        requester=False,
    )

    assert isinstance(req, drms.ExportRequest)
    assert req.wait(timeout=60)
    assert req.has_succeeded()
    assert req.protocol == "fits"

    for record in req.urls.record:
        record = record.lower()
        assert record.startswith("hmi.m_720s_mod")

    for filename in req.urls.filename:
        assert filename.endswith("magnetogram.fits")

    for url in req.urls.url:
        assert url.endswith("magnetogram.fits")


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_export_invalid_process(jsoc_client_export):
    with pytest.raises(ValueError, match="foobar is not one of the allowed processing options"):
        jsoc_client_export.export(
            "aia.lev1_euv_12s[2015-10-17T04:33:30.000/1m@12s][171]{image}",
            process={"foobar": {}},
        )


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_export_email(jsoc_client):
    with pytest.raises(ValueError, match="The email argument is required, when no default email address was set."):
        jsoc_client.export("hmi.v_45s[2016.04.01_TAI/1d@6h]{Dopplergram}")
