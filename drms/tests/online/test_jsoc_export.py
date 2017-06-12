from __future__ import absolute_import, division, print_function

import pytest
import drms


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.parametrize('method', ['url_quick', 'url'])
def test_export_asis_basic(jsoc_client_export, method):
    r = jsoc_client_export.export(
        'hmi.v_avg120[2150]{mean,power}', protocol='as-is', method=method,
        requestor=False)

    assert isinstance(r, drms.ExportRequest)
    assert r.wait(timeout=60)
    assert r.has_succeeded()
    assert r.protocol == 'as-is'
    assert len(r.urls) == 12  # 6 files per segment

    for record in r.urls.record:
        record = record.lower()
        assert record.startswith('hmi.v_avg120[2150]')
        assert (record.endswith('{mean}') or
                record.endswith('{power}'))

    for filename in r.urls.filename:
        assert (filename.endswith('mean.fits') or
                filename.endswith('power.fits'))

    for url in r.urls.url:
        assert (url.endswith('mean.fits') or
                url.endswith('power.fits'))
