from __future__ import absolute_import, division, print_function
import example_helpers

import sys
print('    python: %d.%d.%d' % sys.version_info[:3])

import six
print('       six:', six.__version__)

import numpy
print('     numpy:', numpy.__version__)

import pandas
print('    pandas:', pandas.__version__)

# Use the drms_json.py file from the parent directory
example_helpers.python_path_prepend('..')
import drms_json
print(' drms_json:', drms_json.__version__)
