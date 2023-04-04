"""
===============
Exporting JPEGs
===============

This example shows how to export image data as JPEG file, using the 'jpg'
protocol.

The 'jpg' protocol accepts additional protocol arguments, like color
table, color scaling or pixel binning. For a list of available color
tables, see http://jsoc.stanford.edu/ajax/exportdata.html and select the
JPEG protocol.
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

# Arguments for 'jpg' protocol
jpg_args = {
    "ct": "aia_304.lut",  # color table
    "min": 4,  # min value
    "max": 800,  # max value
    "scaling": "log",  # color scaling
    "size": 2,  # binning (1 -> 4k, 2 -> 2k, 4 -> 1k)
}

# Create download directory if it does not exist yet.
out_dir = Path("downloads")
if not out_dir.exists():
    Path(out_dir).mkdir(parents=True)

###############################################################################
# Construct the DRMS query string: "Series[timespan][wavelength]{data segments}"

qstr = "aia.lev1_euv_12s[2012-08-31T19:48:01Z][304]{image}"
print(f"Data export query:\n  {qstr}\n")

# Submit export request using the 'jpg' protocol with custom protocol_args
print("Submitting export request...")
result = client.export(qstr, protocol="jpg", protocol_args=jpg_args, email=email)

# Print request URL.
print(f"\nRequest URL: {result.request_url}")
print(f"{int(len(result.urls))} file(s) available for download.\n")

# Download selected files.
result.download(out_dir)
print("Download finished.")
print(f"\nDownload directory:\n  {out_dir.resolve()}\n")
