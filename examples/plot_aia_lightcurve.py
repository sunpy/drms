"""
=========================================
Downloading and plotting a AIA lightcurve
=========================================

This example shows how to download AIA data from JSOC and make a lightcurve plot.
"""

import matplotlib.pyplot as plt

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client()

###############################################################################
# Some keywords we are interested in; you can use client.keys(series) to get a
# list of all available keywords of a series.

keys = [
    'T_REC',
    'T_OBS',
    'DATAMIN',
    'DATAMAX',
    'DATAMEAN',
    'DATARMS',
    'DATASKEW',
    'DATAKURT',
    'QUALITY',
]

###############################################################################
# Get detailed information about the series. Some keywords from
# aia.lev1_euv_12s are links to keywords in aia.lev1 and unfortunately some
# entries (like note) are missing for linked keywords, so we are using the
# entries from aia.lev1 in this case.

print('Querying series info...')
series_info = client.info('aia.lev1_euv_12s')
series_info_lev1 = client.info('aia.lev1')
for key in keys:
    linkinfo = series_info.keywords.loc[key].linkinfo
    if linkinfo is not None and linkinfo.startswith('lev1->'):
        note_str = series_info_lev1.keywords.loc[key].note
    else:
        note_str = series_info.keywords.loc[key].note
    print(f'{key:>10} : {note_str}')

###############################################################################
# Construct the DRMS query string: "Series[timespan][wavelength]"

qstr = 'aia.lev1_euv_12s[2014-01-01T00:00:01Z/365d@1d][335]'

# Get keyword values for the selected timespan and wavelength
print(f'Querying keyword data...\n -> {qstr}')
result = client.query(qstr, key=keys)
print(f' -> {len(result)} lines retrieved.')

# Only use entries with QUALITY==0
result = result[result.QUALITY == 0]
print(f' -> {len(result)} lines after QUALITY selection.')

# Convert T_REC strings to datetime and use it as index for the series
result.index = drms.to_datetime(result.T_REC)

###############################################################################
# Create some simple plots

ax = result[['DATAMIN', 'DATAMAX', 'DATAMEAN', 'DATARMS', 'DATASKEW']].plot(figsize=(8, 10), subplots=True)
ax[0].set_title(qstr, fontsize='medium')
plt.tight_layout()
plt.show()
