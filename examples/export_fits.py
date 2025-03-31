"""
======================
Exporting data as fits
======================

This example shows how to submit a data export request using the 'fits'
protocol and how to download the requested files.

Note that the 'as-is' protocol should be used instead of 'fits', if
record keywords in the FITS headers are not needed, as it greatly
reduces the server load.
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

# Use 'as-is' instead of 'fits', if record keywords are not needed in the
# FITS header. This greatly reduces the server load!
export_protocol = "fits"

# Create download directory if it does not exist yet.
out_dir = Path("downloads")
if not out_dir.exists():
    Path(out_dir).mkdir(parents=True)

###############################################################################
# Construct the DRMS query string: "Series[harpnum][timespan]{data segments}"

qstr = "hmi.sharp_720s[12519][2024.12.30_22:24:00_TAI/1d@8h]{continuum, magnetogram, field}"
print(f"Data export query:\n  {qstr}\n")

# Submit export request using the 'fits' protocol
print("Submitting export request...")
result = client.export(qstr, method="url", protocol=export_protocol, email=email)

# Print request URL.
print(f"\nRequest URL: {result.request_url}")
print(f"{len(result.urls)} file(s) available for download.\n")

# Download selected files.
result.download(out_dir)
print("Download finished.")
print(f'\nDownload directory:\n  "{out_dir.absolute()}"\n')
