"""
This example shows how to export movies from image data, using the 'mp4'
protocol. The 'mp4' protocol accepts additional protocol arguments, like
color table, color scaling or pixel binning. For a list of available color
tables, see http://jsoc.stanford.edu/ajax/exportdata.html and select the
MP4 protocol.
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

# Series, timespan and segment
series = 'hmi.m_720s'
tsel = '2014.11.28_00:00:00_TAI/5d@1h'
segment = 'magnetogram'

# Further arguments for 'mp4' protocol
mp4_args = {
    'ct': 'grey.sao',  # color table
    'min': -1500,      # min value
    'max': 1500,       # max value
    'scaling': 'mag',  # color scaling
    'size': 8          # binning (1 -> 4k, 2 -> 2k, 4 -> 1k, 8 -> 512)
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
    email = example_helpers.ask_for_export_email()
if not email or not c.check_email(email):
    raise RuntimeError('Email address is not valid or not registered.')

# Data export query string
qstr = '%s[%s]{%s}' % (series, tsel, segment)
print('Data export query:\n  %s\n' % qstr)

# Submit export request using the 'mp4' protocol with custom protocol_args
print('Submitting export request...')
r = c.export(qstr, protocol='mp4', protocol_args=mp4_args, email=email)
r.wait(sleep=10)

# Print request URL.
print('\nRequest URL: %s' % r.request_url)
print('%d file(s) available for download.\n' % len(r.urls))

# Download movie file only: index=0
r.download(out_dir, 0)
print('Download finished.')
print('\nDownload directory:\n  "%s"\n' % os.path.abspath(out_dir))
