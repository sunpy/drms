"""
This example takes a RequestID of an already existing export request, prints
the corresponding "Request URL" and offers to download the available files.
Note that you can also use RequestIDs from export requests, that were
submitted using the JSOC website.
"""
from __future__ import absolute_import, division, print_function
import os
from six.moves import input
import example_helpers
import drms

# Print the doc string of this example.
print(__doc__)


# Export request ID
request_id = ''

# Create DRMS client, use debug=True to see the query URLs.
c = drms.Client(verbose=True)

# Ask for a RequestID, if it is not set yet.
if not request_id:
    request_id = input('Please enter a RequestID: ')
    print()

# Querying the server using the entered RequestID.
print('Looking up export request "%s"...' % request_id)
r = c.export_from_id(request_id)

# Print request URL and number of available files.
print('\nRequest URL: %s' % r.request_url)
print('%d file(s) available for download.\n' % len(r.urls))

# Ask if the files should be downloaded.
do_download = input('Retrieve all files [y/N]? ')
print()

if do_download.lower() in ['y', 'yes']:
    # Create download directory if it does not exist yet.
    out_dir = os.path.join('downloads', request_id)
    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    # Download all available files.
    r.download(out_dir)
    print('Download finished.')
    print('\nDownload directory:\n  "%s"\n' % os.path.abspath(out_dir))
