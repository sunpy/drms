"""
============================================
Exporting AIA Level 1.5 data using aia_scale
============================================

This example shows how to submit a data export request using the ``aia_scale``
processing option to obtain AIA Level 1.5 data directly from JSOC.
"""

import os
from pathlib import Path

import drms

###############################################################################
# First we will create a `drms.Client`, using the JSOC baseurl.

client = drms.Client()

###############################################################################
# This example requires a registered export email address. You can register
# JSOC exports at: http://jsoc.stanford.edu/ajax/register_email.html
# You must supply your own email.

email = os.environ["JSOC_EMAIL"]

# Create download directory if it does not exist yet.
out_dir = Path("downloads")
if not out_dir.exists():
    Path(out_dir).mkdir(parents=True)

###############################################################################
# Construct the DRMS query string: ``"Series[timespan][wavelength]{data segments}"``
#
# Here we request a single AIA 171 Å image from the ``aia.lev1_euv_12s`` series.

qstr = "aia.lev1_euv_12s[2025-01-01T04:33:30.000][171]{image}"
print(f"Data export query:\n  {qstr}\n")

###############################################################################
# Construct the dictionary specifying the processing command.
#
# JSOC provides ``aia_scale`` routines to scale AIA Level 1 images to Level 1.5,
# standardizing the plate scale to 0.6 arcsec per pixel across all channels,
# correcting roll angle, and updating master pointing calibrations.
#
# Depending on the data series, three variants are available:
#
# * ``aia_scale_aialev1``: for AIA Level 1 series (e.g. ``aia.lev1_euv_12s`` and ``aia.lev1_uv_24s``)
# * ``aia_scale_orig``: for the ``aia.lev1`` series
# * ``aia_scale_other``: for other series such as HMI (e.g. ``hmi.M_45s``)
#
# We pass ``"mpt": "aia.master_pointing3h"`` to apply the 3-hour master pointing
# table, consistent with level 1.5 preparation in ``aiapy`` and IDL ``aia_prep``.
# Optional cutout parameters (``xc``, ``yc``, ``wide``, ``high``) can also be included.
process = {
    "aia_scale_aialev1": {
        "mpt": "aia.master_pointing3h",
    },
}

# Submit export request using the 'fits' protocol
print("Submitting export request...")
result = client.export(
    qstr,
    method="url",
    protocol="fits",
    email=email,
    process=process,
)

# Print request URL.
print(f"\nRequest URL: {result.request_url}")
print(f"{len(result.urls)} file(s) available for download.\n")

# Download selected files.
result.wait()
result.download(out_dir)
print("Download finished.")
print(f'\nDownload directory:\n  "{out_dir.resolve()}"\n')
