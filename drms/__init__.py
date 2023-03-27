"""
drms
====

The ``drms`` library provides an easy-to-use interface for accessing HMI, AIA and MDI data with Python.
It uses the publicly accessible JSOC DRMS server by default, but can also be used with local NetDRMS sites.
More information, including a detailed tutorial, is available in the Documentation.

* Homepage: https://github.com/sunpy/drms
* Documentation: https://docs.sunpy.org/projects/drms/en/stable/
"""

import os


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

from .client import Client, ExportRequest, SeriesInfo
from .config import ServerConfig, register_server
from .exceptions import DrmsError, DrmsExportError, DrmsOperationNotSupported, DrmsQueryError
from .json import HttpJsonClient, HttpJsonRequest, const
from .utils import to_datetime
from .version import version as __version__

__all__ = [
    "__bibtex__",
    "__citation__",
    "__version__",
    "Client",
    "const",
    "DrmsError",
    "DrmsExportError",
    "DrmsOperationNotSupported",
    "DrmsQueryError",
    "ExportRequest",
    "HttpJsonClient",
    "HttpJsonRequest",
    "register_server",
    "SeriesInfo",
    "ServerConfig",
    "to_datetime",
]
