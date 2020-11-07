from collections import OrderedDict

import pandas as pd

import drms


def test_parse_keywords():
    info = [
        {
            'recscope': 'variable',
            'units': 'none',
            'name': 'cparms_sg000',
            'defval': 'compress Rice',
            'note': '',
            'type': 'string',
        },
        {
            'recscope': 'variable',
            'units': 'none',
            'name': 'mean_bzero',
            'defval': '0',
            'note': '',
            'type': 'double',
        },
        {
            'recscope': 'variable',
            'units': 'none',
            'name': 'mean_bscale',
            'defval': '0.25',
            'note': '',
            'type': 'double',
        },
        {
            'recscope': 'variable',
            'units': 'TAI',
            'name': 'MidTime',
            'defval': '-4712.01.01_11:59_TAI',
            'note': 'Midpoint of averaging interval',
            'type': 'time',
        },
    ]
    exp = OrderedDict(
        [
            ('name', ['cparms_sg000', 'mean_bzero', 'mean_bscale', 'MidTime']),
            ('type', ['string', 'double', 'double', 'time']),
            ('recscope', ['variable', 'variable', 'variable', 'variable']),
            ('defval', ['compress Rice', '0', '0.25', '-4712.01.01_11:59_TAI']),
            ('units', ['none', 'none', 'none', 'TAI']),
            ('note', ['', '', '', 'Midpoint of averaging interval']),
            ('linkinfo', [None, None, None, None]),
            ('is_time', [False, False, False, True]),
            ('is_integer', [False, False, False, False]),
            ('is_real', [False, True, True, False]),
            ('is_numeric', [False, True, True, False]),
        ]
    )

    exp = pd.DataFrame(data=exp)
    exp.index = exp.pop('name')
    assert drms.SeriesInfo._parse_keywords(info).equals(exp)


def test_parse_links():
    links = [
        {'name': 'BHARP', 'kind': 'DYNAMIC', 'note': 'Bharp', 'target': 'hmi.Bharp_720s'},
        {'name': 'MHARP', 'kind': 'DYNAMIC', 'note': 'Mharp', 'target': 'hmi.Mharp_720s'},
    ]
    exp = OrderedDict(
        [
            ('name', ['BHARP', 'MHARP']),
            ('target', ['hmi.Bharp_720s', 'hmi.Mharp_720s']),
            ('kind', ['DYNAMIC', 'DYNAMIC']),
            ('note', ['Bharp', 'Mharp']),
        ]
    )
    exp = pd.DataFrame(data=exp)
    exp.index = exp.pop('name')
    assert drms.SeriesInfo._parse_links(links).equals(exp)


def test_parse_segments():
    segments = [
        {
            'type': 'int',
            'dims': 'VARxVAR',
            'units': 'Gauss',
            'protocol': 'fits',
            'note': 'magnetogram',
            'name': 'magnetogram',
        },
        {
            'type': 'char',
            'dims': 'VARxVAR',
            'units': 'Enumerated',
            'protocol': 'fits',
            'note': 'Mask for the patch',
            'name': 'bitmap',
        },
        {
            'type': 'int',
            'dims': 'VARxVAR',
            'units': 'm/s',
            'protocol': 'fits',
            'note': 'Dopplergram',
            'name': 'Dopplergram',
        },
    ]
    exp = OrderedDict(
        [
            ('name', ['magnetogram', 'bitmap', 'Dopplergram']),
            ('type', ['int', 'char', 'int']),
            ('units', ['Gauss', 'Enumerated', 'm/s']),
            ('protocol', ['fits', 'fits', 'fits']),
            ('dims', ['VARxVAR', 'VARxVAR', 'VARxVAR']),
            ('note', ['magnetogram', 'Mask for the patch', 'Dopplergram']),
        ]
    )

    exp = pd.DataFrame(data=exp)
    exp.index = exp.pop('name')
    assert drms.SeriesInfo._parse_segments(segments).equals(exp)


def test_repr():
    info = {
        'primekeys': ['CarrRot', 'CMLon'],
        'retention': 1800,
        'tapegroup': 1,
        'archive': 1,
        'primekeysinfo': [],
        'unitsize': 1,
        'note': 'Temporal averages of HMI Vgrams over 1/3 CR',
        'dbindex': [None],
        'links': [],
        'segments': [],
        'keywords': [],
    }
    assert repr(drms.SeriesInfo(info)) == '<SeriesInfo>'
    assert repr(drms.SeriesInfo(info, 'hmi')) == '<SeriesInfo: hmi>'
