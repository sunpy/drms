from __future__ import absolute_import, division, print_function
import matplotlib.pyplot as plt
from astropy.io import fits
import example_helpers
import drms


# Series name, carrington rotation and data segment
series = 'hmi.synoptic_mr_720s'
cr = 2150
segname = 'synopMr'

# DRMS-Server URL (or shortcut) and data url (if any) for the data segment
drms_url, data_url = 'jsoc', 'http://jsoc.stanford.edu'
#drms_url, data_url = 'kis', ''

# DRMS query string
qstr = '%s[%s]' % (series, cr)


# Create DRMS JSON client, use debug=True to see the query URLs
c = drms.Client(drms_url)

# Send request to the DRMS server
print('Querying keyword data...\n -> %s' % qstr)
k, s = c.query(qstr, key=drms.const.all, seg=segname)
print(' -> %d lines retrieved.' % len(k))

# Use only the first line of the query result
k = k.iloc[0]
fname = data_url + s[segname][0]

# Read the data segment
# Note: HTTP downloads get cached in ~/.astropy/cache/downloads
print('Reading data from %r...' % fname)
a = fits.getdata(fname)
ny, nx = a.shape

# Convert pixel to world coordinates using WCS keywords
xmin = (1 - k.CRPIX1)*k.CDELT1 + k.CRVAL1
xmax = (nx - k.CRPIX1)*k.CDELT1 + k.CRVAL1
ymin = (1 - k.CRPIX2)*k.CDELT2 + k.CRVAL2
ymax = (ny - k.CRPIX2)*k.CDELT2 + k.CRVAL2

# Convert to Carrington longitude
xmin = k.LON_LAST - xmin
xmax = k.LON_LAST - xmax

# Compute the plot extent used with imshow
extent = (xmin - abs(k.CDELT1)/2, xmax + abs(k.CDELT1)/2,
          ymin - abs(k.CDELT2)/2, ymax + abs(k.CDELT2)/2)

# Aspect ratio for imshow in respect to the extent computed above
aspect = abs((xmax - xmin)/nx * ny/(ymax - ymin))

# Create plot
fig, ax = plt.subplots(1, 1, figsize=(13.5, 6))
ax.set_title('%s, Time: %s ... %s' % (qstr, k.T_START, k.T_STOP),
             fontsize='medium')
ax.imshow(a, vmin=-300, vmax=300, origin='lower', interpolation='nearest',
          cmap='gray', extent=extent, aspect=aspect)
ax.invert_xaxis()
ax.set_xlabel('Carrington longitude')
ax.set_ylabel('Sine latitude')
fig.tight_layout()

plt.show()
