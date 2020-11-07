"""
==================================
Exporting from existing RequestIDs
==================================

This example takes a RequestID of an already existing export request, prints
the corresponding "Request URL" and downloads the available files.

Note that you can also use RequestIDs from export requests, that were
submitted using the JSOC website.
"""

import os

import drms

###############################################################################
# Create DRMS client, uses the JSOC baseurl by default, set debug=True to see the DRMS query URLs.

client = drms.Client(verbose=True)

# Export request ID
request_id = 'JSOC_20201101_198'

# Querying the server using the entered RequestID.
print(f'Looking up export request {request_id}...')
result = client.export_from_id(request_id)

# Print request URL and number of available files.
print(f'\nRequest URL: {result.request_url}')
print(f'{int(len(result.urls))} file(s) available for download.\n')

# Create download directory if it does not exist yet.
out_dir = os.path.join('downloads', request_id)
if not os.path.exists(out_dir):
    os.makedirs(out_dir)

# Download all available files.
result.download(out_dir)
print('Download finished.')
print(f'\nDownload directory:\n  {os.path.abspath(out_dir)}\n')
