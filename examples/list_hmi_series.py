from __future__ import absolute_import, division, print_function
import textwrap
import example_helpers
import drms


# Set to True, to list additional information
full_output = False

# Create DRMS JSON client, use debug=True to see the query URLs
c = drms.Client()

# Get all available HMI series
s = c.series(r'hmi\.', full=full_output)

if not full_output:
    # Print only the series names
    for name in s:
        print(name)
else:
    # Print series names, pkeys and notes
    for i in s.index:
        print('Series:', s.name[i])
        if c.server.url_show_series_wrapper is None:
            # JSOC's show_series wrapper currently does not support primekeys
            print(' Pkeys:', ', '.join(s.primekeys[i]))
        print(' Notes:', ('\n' + 8*' ').join(textwrap.wrap(s.note[i])))
        print()
