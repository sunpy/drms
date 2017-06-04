from __future__ import absolute_import, division, print_function

import os


# Package directory, i.e. the parent directory in respect to this file
pkg_dir = os.path.dirname(os.path.dirname(__file__))


try:
    import pytest
except ImportError:
    def run_tests(extra_args=None):
        raise ImportError('pytest is needed to run tests')
else:
    def run_tests(extra_args=None):
        args = []
        if extra_args is not None:
            args += extra_args
        args += [pkg_dir]
        print('running: pytest ' + ' '.join(args))
        return pytest.main(args)
