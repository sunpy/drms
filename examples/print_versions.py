from __future__ import absolute_import, division, print_function
import sys
import argparse
import example_helpers

parser = argparse.ArgumentParser()
parser.add_argument('--verbose', '-v', action='store_true')
args = parser.parse_args()

print('    python: %d.%d.%d' % sys.version_info[:3])
if args.verbose:
    print('        ->', sys.executable)

import six
print('       six:', six.__version__)
if args.verbose:
    print('        ->', six.__file__)

import numpy
print('     numpy:', numpy.__version__)
if args.verbose:
    print('        ->', numpy.__file__)

import pandas
print('    pandas:', pandas.__version__)
if args.verbose:
    print('        ->', pandas.__file__)

# Use the drms_json.py file from the parent directory
example_helpers.python_path_prepend('..')
import drms_json
print(' drms_json:', drms_json.__version__)
if args.verbose:
    print('        ->', drms_json.__file__)
