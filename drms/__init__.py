"""
drms
====

The ``drms`` library provides an easy-to-use interface for accessing HMI, AIA and MDI data with Python.
It uses the publicly accessible JSOC DRMS server by default, but can also be used with local NetDRMS sites.
More information, including a detailed tutorial, is available in the Documentation.

* Homepage: https://github.com/sunpy/drms
* Documentation: https://docs.sunpy.org/projects/drms/en/stable/
"""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

from .client import Client, ExportRequest, SeriesInfo
from .config import ServerConfig, register_server
from .exceptions import DrmsError, DrmsExportError, DrmsOperationNotSupported, DrmsQueryError
from .json import HttpJsonClient, HttpJsonRequest, JsocInfoConstants
from .utils import to_datetime
from .version import version as __version__


def _get_bibtex():
    import textwrap

    # Set the bibtex entry to the article referenced in CITATION.rst
    citation_file = Path(__file__).parent / "CITATION.rst"
    # Explicitly specify UTF-8 encoding in case the system's default encoding is problematic
    with citation_file.open(encoding="utf-8") as citation:
        # Extract the first bibtex block:
        ref = citation.read().partition(".. code:: bibtex\n\n")[2]
        lines = ref.split("\n")
        # Only read the lines which are indented
        lines = lines[: [line.startswith("    ") for line in lines].index(False)]
        return textwrap.dedent("\n".join(lines))


__citation__ = __bibtex__ = _get_bibtex()

__all__ = [
    "Client",
    "DrmsError",
    "DrmsExportError",
    "DrmsOperationNotSupported",
    "DrmsQueryError",
    "ExportRequest",
    "HttpJsonClient",
    "HttpJsonRequest",
    "JsocInfoConstants",
    "SeriesInfo",
    "ServerConfig",
    "__bibtex__",
    "__citation__",
    "__version__",
    "logger",
    "register_server",
    "to_datetime",
]
