from __future__ import absolute_import, division, print_function

# Use the drms_json.py file from the parent directory
import example_helpers
example_helpers.python_path_prepend('..')

import drms_json as drms


# Create DRMS JSON client, use debug=True to see the query URLs
c = drms.Client()

# Get all available HMI series
s = c.series(r'hmi\.')

# Print series names, pkeys and notes
for name, pkeys, notes in s.values:
    print('Series:', name)
    print(' Pkeys:', ', '.join(pkeys))
    print(' Notes:', notes)
    print()
