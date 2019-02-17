# Copyright (c) 2014-2019 Kolja Glogowski and others.
# See AUTHORS.txt for a list of contributors.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

"""
Access HMI, AIA and MDI data with Python

The latest release is avaiable at https://github.com/sunpy/drms .
"""

from __future__ import absolute_import, division, print_function

from . import config, error, json, client, utils
from .error import *
from .client import *
from .utils import *
from .json import const

# Keep the following three lines like this, so that versioneer does not add
# them again when running "python versioneer.py setup".
from ._version import get_versions
__version__ = get_versions()['version']
del get_versions

__all__ = ['const']
__all__ += error.__all__
__all__ += client.__all__
__all__ += utils.__all__

# We imported all public classes and functions from submodules. The submodule
# symbols themselves are now removed to keep the package namespace cleaner.
del config
del error
del json
del utils
del client
