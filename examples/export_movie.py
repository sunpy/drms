"""
=================
Exporting a movie
=================

This example shows how to export movies from image data, using the 'mp4'
protocol.

The 'mp4' protocol accepts additional protocol arguments, like color
table, color scaling or pixel binning. For a list of available color
tables, see http://jsoc.stanford.edu/ajax/exportdata.html and select the
MP4 protocol.
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
# Construct the DRMS query string: "Series[timespan]{segment}"

qstr = "hmi.m_720s[2014.11.28_00:00:00_TAI/5d@1h]{magnetogram}"
print(f"Data export query:\n  {qstr}\n")

###############################################################################
# Arguments for 'mp4' protocol

mp4_args = {
    "ct": "grey.sao",  # color table
    "min": -1500,  # min value
    "max": 1500,  # max value
    "scaling": "mag",  # color scaling
    "size": 8,  # binning (1 -> 4k, 2 -> 2k, 4 -> 1k, 8 -> 512)
}

# Submit export request using the 'mp4' protocol with custom protocol_args
print("Submitting export request...")
result = client.export(qstr, protocol="mp4", protocol_args=mp4_args, email=email)
result.wait(sleep=10)

# Print request URL.
print(f"\nRequest URL: {result.request_url}")
print(f"{len(result.urls)} file(s) available for download.\n")

# Download movie file only: index=0
result.download(out_dir, index=0)
print("Download finished.")
print(f"\nDownload directory:\n  {out_dir.resolve()}\n")
