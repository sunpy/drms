"""
This example shows how to submit an 'url_quick' / 'as-is' data export
request to JSOC and how to download the requested files. The export protocol
'as-is', should be preferred over other protocols, because it minimizes the
server load. The only reason to use protocol='fits' is, when keywords in the
FITS header are really needed.
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

# Series, harpnum, timespan and segment selection
series = 'hmi.sharp_720s'
harpnum = 4864
tsel = '2014.11.29_00:00:00_TAI/3d@12h'
segments = ['continuum', 'magnetogram', 'field']

# Download directory
out_dir = os.path.join('downloads', 'sharp_%d_as_is' % harpnum)

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
qstr = '%s[%d][%s]{%s}' % (series, harpnum, tsel, ','.join(segments))
print('Data export query:\n  %s\n' % qstr)

# Submit export request, defaults to method='url_quick' and protocol='as-is'
print('Submitting export request...')
r = c.export(qstr, email=email)
print('%d file(s) available for download.\n' % len(r.urls))

# Download selected files.
r.download(out_dir)
print('Download finished.')
print('\nDownload directory:\n  "%s"\n' % os.path.abspath(out_dir))
