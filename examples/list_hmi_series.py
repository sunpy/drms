"""
==============================================
Print all HMI series and prime keys with notes
==============================================

This example shows how to find and display the HMI series names, prime keys and corresponding notes.
"""
import textwrap

import drms

###############################################################################
# Make the basic query.
# Create DRMS JSON client, use debug=True to see the query URLs
client = drms.Client()

# Get all available HMI series
hmi_series = client.series(r'hmi\.', full=True)

# Print series names, prime-keys (pkeys) and notes
for series in hmi_series.index:
    print('Series:', hmi_series.name[series])
    print(' Notes:', (f'\n{8 * " "}').join(textwrap.wrap(hmi_series.note[series])))
