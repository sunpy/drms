"""
This example shows how to export image data as JPEG file, using the 'jpg'
protocol. The 'jpg' protocol accepts additional protocol arguments, like
color table, color scaling or pixel binning. For a list of available color
tables, see http://jsoc.stanford.edu/ajax/exportdata.html and select the
JPEG protocol.
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

# Series, timespan, wavelength and segment
series = 'aia.lev1_euv_12s'
tsel = '2012-08-31T19:48:01Z'
wavelen = 304
segment = 'image'

# Further arguments for 'jpg' protocol
jpg_args = {
    'ct': 'aia_304.lut',  # color table
    'min': 4,             # min value
    'max': 800,           # max value
    'scaling': 'log',     # color scaling
    'size': 2             # binning (1 -> 4k, 2 -> 2k, 4 -> 1k)
}

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
qstr = '%s[%s][%d]{%s}' % (series, tsel, wavelen, segment)
print('Data export query:\n  %s\n' % qstr)

# Submit export request using the 'jpg' protocol with custom protocol_args
print('Submitting export request...')
r = c.export(qstr, protocol='jpg', protocol_args=jpg_args, email=email)

# Print request URL.
print('\nRequest URL: %s' % r.request_url)
print('%d file(s) available for download.\n' % len(r.urls))

# Download selected files.
r.download(out_dir)
print('Download finished.')
print('\nDownload directory:\n  "%s"\n' % os.path.abspath(out_dir))
