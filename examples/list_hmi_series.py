from __future__ import print_function, division
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
