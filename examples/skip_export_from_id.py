"""
==================================
Exporting from existing RequestIDs
==================================

This example takes a RequestID of an already existing export request, prints
the corresponding "Request URL" and downloads the available files.

Note that you can also use RequestIDs from export requests, that were
submitted using the JSOC website.
"""

from pathlib import Path

import drms

###############################################################################
# First we will create a `drms.Client`, using the JSOC baseurl.

client = drms.Client()

# Export request ID
request_id = "JSOC_20201101_198"

# Querying the server using the entered RequestID.
print(f"Looking up export request {request_id}...")
result = client.export_from_id(request_id)

# Print request URL and number of available files.
print(f"\nRequest URL: {result.request_url}")
print(f"{len(result.urls)} file(s) available for download.\n")

# Create download directory if it does not exist yet.
out_dir = Path("downloads") / request_id
if not out_dir.exists():
    Path(out_dir).mkdir(parents=True)

# Download all available files.
result.download(out_dir)
print("Download finished.")
print(f"\nDownload directory:\n  {Path.resolve(out_dir)}\n")
