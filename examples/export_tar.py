"""
This example shows how to submit a data export request using the 'url-tar'
method, which provides a single TAR archive containing all requested files.
Here we use this method to download data from the 'hmi.rdvflows_fd15_frame'
series, which stores directories of text files for each record. This is
currently the only way to download directory data segments using the Python
DRMS client. The export protocol in this case is 'as-is'. You might change the
protocol to 'fits', if you are downloading FITS files instead of text files.
"""
from __future__ import absolute_import, division, print_function
import os
import example_helpers
import drms

# Print the doc string of this example.
print(__doc__)


# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
#
# You will be asked for your registered email address during execution of
# this example. If you don't want to enter it every time you run this script,
# you can set the environment variable JSOC_EXPORT_EMAIL or the variable
# below to your registered email address.
email = ''

# Series, Carrington rotation, Carrington longitude and data segments
series = 'hmi.rdvflows_fd15_frame'
cr = 2150
cmlon = 360
segments = ['Ux', 'Uy']

# Download directory
out_dir = 'downloads'

# Create download directory if it does not exist yet.
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

# Check if the email address was set at the top of this script. If not, ask for
# a registered email address.
if not email:
    email = example_helpers.get_export_email()
if not email or not c.check_email(email):
    raise RuntimeError('Email address is not valid or not registered.')

# Data export query string
qstr = '%s[%d][%d]{%s}' % (series, cr, cmlon, ','.join(segments))
print('Data export query:\n  %s\n' % qstr)

# Submit export request using the 'url-tar' method, protocol default: 'as-is'
print('Submitting export request...')
r = c.export(qstr, method='url-tar', email=email)

# Print request URL.
print('\nRequest URL: %s' % r.request_url)
print('%d file(s) available for download.\n' % len(r.urls))

# Download selected files.
dr = r.download(out_dir)
print('Download finished.')
print('\nDownloaded file:\n  "%s"\n' % dr.download[0])
