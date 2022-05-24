"""
drms
====

The drms library provides an easy-to-use interface for accessing HMI, AIA and MDI data with Python.
It uses the publicly accessible JSOC DRMS server by default, but can also be used with local NetDRMS sites.
More information, including a detailed tutorial, is available in the Documentation.

* Homepage: https://github.com/sunpy/drms
* Documentation: https://docs.sunpy.org/projects/drms/en/stable/
"""

import os
import sys

# Enforce Python version check during package import.
# Must be done before any drms imports
__minimum_python_version__ = "3.7"


class UnsupportedPythonError(Exception):
    """
    Running on an unsupported version of Python.
    """


if sys.version_info < tuple(int(val) for val in __minimum_python_version__.split(".")):
    # This has to be .format to keep backwards compatibly.
    raise UnsupportedPythonError("sunpy does not support Python < {}".format(__minimum_python_version__))


def _get_bibtex():
    import textwrap

    # Set the bibtex entry to the article referenced in CITATION.rst
    citation_file = os.path.join(os.path.dirname(__file__), "CITATION.rst")

    # Explicitly specify UTF-8 encoding in case the system's default encoding is problematic
    with open(citation_file, encoding="utf-8") as citation:
        # Extract the first bibtex block:
        ref = citation.read().partition(".. code:: bibtex\n\n")[2]
        lines = ref.split("\n")
        # Only read the lines which are indented
        lines = lines[: [line.startswith("    ") for line in lines].index(False)]
        ref = textwrap.dedent("\n".join(lines))
    return ref


__citation__ = __bibtex__ = _get_bibtex()

# DRMS imports to collapse the namespace
from .client import *
from .config import *
from .exceptions import *
from .json import *
from .utils import *
from .version import version as __version__
