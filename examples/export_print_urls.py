"""
This example prints the download URLs for files returned from an 'as-is' data
export request. Note that there is no "Request URL" for method 'url_quick'.
"""
from __future__ import absolute_import, division, print_function
import example_helpers
import drms

# Print the doc string of this example.
print(__doc__)


# If you don't want to enter your email address during program execution, you
# can set this variable to the email address you have registered for JSOC data
# exports. If you have not registered your email yet, you can do this on the
# JSOC website at: http://jsoc.stanford.edu/ajax/register_email.html
email = ''

# Data export query string
qstr = 'hmi.ic_720s[2015.01.01_00:00:00_TAI/10d@1d]{continuum}'

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

# Check if the email address was set at the top of this script. If not, ask for
# a registered email address.
if not email:
    email = example_helpers.ask_for_export_email()
if not email or not c.check_email(email):
    raise RuntimeError('Email address is not valid or not registered.')

# Submit export request, defaults to method='url_quick' and protocol='as-is'
print('Data export query:\n  %s\n' % qstr)
print('Submitting export request...')
r = c.export(qstr, email=email)
print('%d file(s) available for download.\n' % len(r.urls))

# Print download URLs.
for i, row in r.urls[['record', 'url']].iterrows():
    print('REC: %s' % row.record)
    print('URL: %s\n' % row.url)
