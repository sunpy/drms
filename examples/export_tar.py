"""
====================================
Downloading data as a tar collection
====================================

This example shows how to submit a data export request using the 'url-tar'
method, which provides a single TAR archive containing all requested files.

Here we use this method to download data from the
'hmi.rdvflows_fd15_frame' series, which stores directories of text files
for each record. This is currently the only way to download directory
data segments using the Python DRMS client. The export protocol in this
case is 'as-is'. You might change the protocol to 'fits', if you are
downloading FITS files instead of text files.
"""

import os
from pathlib import Path

import drms

###############################################################################
# First we will create a `drms.Client`, using the JSOC baseurl.

client = drms.Client()

# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
# You must supply your own email.
email = os.environ["JSOC_EMAIL"]

# Create download directory if it does not exist yet.
out_dir = Path("downloads")
if not out_dir.exists():
    Path(out_dir).mkdir(parents=True)

###############################################################################
# Construct the DRMS query string: "Series[Carrington rotation][Carrington longitude]{data segments}"

qstr = "hmi.rdvflows_fd15_frame[2150][360]{Ux, Uy}"
print(f"Data export query:\n  {qstr}\n")

# Submit export request using the 'url-tar' method, protocol default: 'as-is'
print("Submitting export request...")
result = client.export(qstr, method="url-tar", email=email)

# Print request URL.
print(f"\nRequest URL: {result.request_url}")
print(f"{len(result.urls)} file(s) available for download.\n")

# Download selected files.
dr = result.download(out_dir)
print("Download finished.")
print(f'\nDownloaded file:\n  "{dr.download[0]}"\n')
