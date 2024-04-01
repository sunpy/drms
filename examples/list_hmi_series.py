"""
==============================================
Print all HMI series and prime keys with notes
==============================================

This example shows how to find and display the HMI series names, prime keys and corresponding notes.
"""

import textwrap

import drms

###############################################################################
# First we will create a `drms.Client`, using the JSOC baseurl.
client = drms.Client()

###############################################################################
# Get all available HMI series and print their names, prime keys and notes.

hmi_series = client.series(regex=r"hmi\.", full=True)

# Print series names, prime-keys (pkeys) and notes
for series in hmi_series.index:
    print("Series:", hmi_series.name[series])
    print(" Notes:", (f'\n{8 * " "}').join(textwrap.wrap(hmi_series.note[series])))
