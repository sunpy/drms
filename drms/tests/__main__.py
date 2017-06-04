from __future__ import absolute_import, division, print_function

import sys
from ._runner import run_tests

sys.exit(run_tests(sys.argv[1:]))
