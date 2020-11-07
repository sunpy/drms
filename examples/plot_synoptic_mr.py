"""
============================================
Downloading and plotting a HMI synoptic data
============================================

This example shows how to download HMI synoptic data from JSOC and make a plot.
"""

import matplotlib.pyplot as plt

from astropy.io import fits

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client()

###############################################################################
# Construct the DRMS query string: "Series[Carrington rotation]"

qstr = 'hmi.synoptic_mr_720s[2150]'

# Send request to the DRMS server
print('Querying keyword data...\n -> {qstr}')
segname = 'synopMr'
results, filenames = client.query(qstr, key=drms.const.all, seg=segname)
print(f' -> {len(results)} lines retrieved.')

# Use only the first line of the query result
results = results.iloc[0]
fname = f'http://jsoc.stanford.edu{filenames[segname][0]}'

# Read the data segment
# Note: HTTP downloads get cached in ~/.astropy/cache/downloads
print(f'Reading data from {fname}...')
a = fits.getdata(fname)
ny, nx = a.shape

###############################################################################
# Now to plot the image.

# Convert pixel to world coordinates using WCS keywords
xmin = (1 - results.CRPIX1) * results.CDELT1 + results.CRVAL1
xmax = (nx - results.CRPIX1) * results.CDELT1 + results.CRVAL1
ymin = (1 - results.CRPIX2) * results.CDELT2 + results.CRVAL2
ymax = (ny - results.CRPIX2) * results.CDELT2 + results.CRVAL2

# Convert to Carrington longitude
xmin = results.LON_LAST - xmin
xmax = results.LON_LAST - xmax

# Compute the plot extent used with imshow
extent = (
    xmin - abs(results.CDELT1) / 2,
    xmax + abs(results.CDELT1) / 2,
    ymin - abs(results.CDELT2) / 2,
    ymax + abs(results.CDELT2) / 2,
)

# Aspect ratio for imshow in respect to the extent computed above
aspect = abs((xmax - xmin) / nx * ny / (ymax - ymin))

# Create plot
fig, ax = plt.subplots(1, 1, figsize=(13.5, 6))
ax.set_title(f'{qstr}, Time: {results.T_START} ... {results.T_STOP}', fontsize='medium')
ax.imshow(
    a, vmin=-300, vmax=300, origin='lower', interpolation='nearest', cmap='gray', extent=extent, aspect=aspect,
)
ax.invert_xaxis()
ax.set_xlabel('Carrington longitude')
ax.set_ylabel('Sine latitude')
fig.tight_layout()

plt.show()
