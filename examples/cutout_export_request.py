"""
===================================
Exporting data with cutout requests
===================================

This example shows how to submit a data export request with a cutout request using the ``im_patch`` command.
"""

import os

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client(verbose=True)

# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
# You must supply your own email.
email = os.environ["JSOC_EMAIL"]

# Download directory
out_dir = os.path.join('downloads')

# Create download directory if it does not exist yet.
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

###############################################################################
# Construct the DRMS query string: "Series[timespan][wavelength]{data segments}"

qstr = 'aia.lev1_euv_12s[2015-10-17T04:33:30.000/1m@12s][171]{image}'
print(f'Data export query:\n  {qstr}\n')

###############################################################################
# Construct the dictionary specifying that we want to request a cutout.
# This is done via the ``im_patch`` command.
# We request a 345.6 arcsecond cutout (on both sides) centered on the coordinate (-517.2, -246) arcseconds as defined in the helioprojective frame of SDO at time ``t_ref``.
# The ``t`` controls whether tracking is disabled (``1``) or enabled (``0``).
# ``r`` controls the use of sub-pixel registration.
# ``c`` controls whether off-limb pixels are filled with NaNs.
# For additional details about ``im_patch``, see the `documentation <http://jsoc.stanford.edu/doxygen_html/group__im__patch.html>`_.
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

# Submit export request using the 'fits' protocol
print('Submitting export request...')
result = client.export(
    qstr,
    method='url',
    protocol='fits',
    email=email,
    process=process,
)

# Print request URL.
print(f'\nRequest URL: {result.request_url}')
print(f'{int(len(result.urls))} file(s) available for download.\n')

# Download selected files.
result.wait()
result.download(out_dir)
print('Download finished.')
print(f'\nDownload directory:\n  "{os.path.abspath(out_dir)}"\n')
