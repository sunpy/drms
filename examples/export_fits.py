"""
This example shows how to submit a data export request using the 'fits'
protocol and how to download the requested files. Note that the 'as-is'
protocol should be used instead of 'fits', if record keywords in the FITS
headers are not needed, as it greatly reduces the server load.
"""
from __future__ import absolute_import, division, print_function
import os
import example_helpers
import drms

# Print the doc string of this example.
print(__doc__)


# If you don't want to enter your email address during program execution, you
# can set this variable to the email address you have registered for JSOC data
# exports. If you have not registered your email yet, you can do this on the
# JSOC website at: http://jsoc.stanford.edu/ajax/register_email.html
email = ''

# Use 'as-is' instead of 'fits', if record keywords are not needed in the
# FITS header. This greatly reduces the server load!
export_protocol = 'fits'
#export_protocol = 'as-is'

# Series, harpnum, timespan and segment selection
series = 'hmi.sharp_720s'
harpnum = 4864
tsel = '2014.11.30_00:00:00_TAI/1d@8h'
segments = ['continuum', 'magnetogram', 'field']

# Download directory
out_dir = os.path.join('downloads', 'sharp_%d' % harpnum)

# Create download directory if it does not exist yet.
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

# Check if the email address was set at the top of this script. If not, ask for
# a registered email address.
if not email:
    email = example_helpers.ask_for_export_email()
if not email or not c.check_email(email):
    raise RuntimeError('Email address is not valid or not registered.')

# Data export query string
qstr = '%s[%d][%s]{%s}' % (series, harpnum, tsel, ','.join(segments))
print('Data export query:\n  %s\n' % qstr)

# Submit export request using the 'fits' protocol
print('Submitting export request...')
r = c.export(qstr, method='url', protocol=export_protocol, email=email)

# Print request URL.
print('\nRequest URL: %s' % r.request_url)
print('%d file(s) available for download.\n' % len(r.urls))

# Download selected files.
r.download(out_dir)
print('Download finished.')
print('\nDownload directory:\n  "%s"\n' % os.path.abspath(out_dir))
