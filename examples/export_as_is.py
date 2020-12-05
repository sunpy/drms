"""
=========================
Exporting data as 'as-is'
=========================

This example shows how to submit an 'url_quick' / 'as-is' data export request
to JSOC and how to download the requested files.

The export protocol 'as-is', should be preferred over other protocols,
because it minimizes the server load. The only reason to use
protocol='fits' is, when keywords in the FITS header are really needed.
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
# Construct the DRMS query string: "Series[harpnum][timespan]{data segments}"

qstr = 'hmi.sharp_720s[7451][2020.09.27_00:00:00_TAI]{continuum, magnetogram, field}'
print(f'Data export query:\n  {qstr}\n')

# Submit export request, defaults to method='url_quick' and protocol='as-is'
print('Submitting export request...')
result = client.export(qstr, email=email)
print(f'{int(len(result.urls))} file(s) available for download.\n')

# Download selected files.
result.download(out_dir)
print('Download finished.')
print(f'\nDownload directory:\n  "{os.path.abspath(out_dir)}"\n')
