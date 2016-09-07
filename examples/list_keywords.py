from __future__ import absolute_import, division, print_function

# Use the drms_json.py file from the parent directory
import example_helpers
example_helpers.python_path_prepend('..')

import drms_json as drms


# DRMS series name
series = 'hmi.v_45s'

# Create DRMS JSON client, use debug=True to see the query URLs
c = drms.Client()

# Query series info
si = c.info(series)

# Print keyword info
print('Listing keywords for "%s":\n' % si.name)
for k in sorted(si.keywords.index):
    ki = si.keywords.loc[k]
    print(k)
    print('  type ....... %s ' % ki.type)
    print('  recscope ... %s ' % ki.recscope)
    print('  defval ..... %s ' % ki.defval)
    print('  units ...... %s ' % ki.units)
    print('  note ....... %s ' % ki.note)
    print()
