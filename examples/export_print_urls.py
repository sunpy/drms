"""
==============================
Getting the urls of a download
==============================

This example prints the download URLs for files returned from an 'as-is' data
export request.

Note that there is no "Request URL" for method 'url_quick'.
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

###############################################################################
# Construct the DRMS query string: "Series[timespan][wavelength]"

qstr = 'hmi.ic_720s[2015.01.01_00:00:00_TAI/10d@1d]{continuum}'

# Submit export request, defaults to method='url_quick' and protocol='as-is'
print(f'Data export query:\n  {qstr}\n')
print('Submitting export request...')
result = client.export(qstr, email=email)
print(f'len(r.urls) file(s) available for download.\n')

# Print download URLs.
for _, row in result.urls[['record', 'url']].iterrows():
    print(f'REC: {row.record}')
    print(f'URL: {row.url}\n')
