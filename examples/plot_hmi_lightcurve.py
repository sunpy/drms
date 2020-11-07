"""
=========================================
Downloading and plotting a HMI lightcurve
=========================================

This example shows how to download HMI data from JSOC and make a lightcurve plot.
"""

import matplotlib.pyplot as plt

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client()

###############################################################################
# Construct the DRMS query string: "Series[timespan]"

qstr = f'hmi.ic_720s[2010.05.01_TAI-2016.04.01_TAI@6h]'

# Send request to the DRMS server
print('Querying keyword data...\n -> {qstr}')
result = client.query(qstr, key=['T_REC', 'DATAMEAN', 'DATARMS'])
print(f' -> {int(len(result))} lines retrieved.')

###############################################################################
# Now to plot the image.

# Convert T_REC strings to datetime and use it as index for the series
result.index = drms.to_datetime(result.pop('T_REC'))

# Note: DATARMS contains the standard deviation, not the RMS!
t = result.index
avg = result.DATAMEAN / 1e3
std = result.DATARMS / 1e3

# Create plot
fig, ax = plt.subplots(1, 1, figsize=(15, 7))
ax.set_title(qstr, fontsize='medium')
ax.fill_between(
    t, avg + std, avg - std, edgecolor='none', facecolor='b', alpha=0.3, interpolate=True,
)
ax.plot(t, avg, color='b')
ax.set_xlabel('Time')
ax.set_ylabel('Disk-averaged continuum intensity [kDN/s]')
fig.tight_layout()

plt.show()
