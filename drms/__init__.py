"""
drms
====

Access HMI, AIA and MDI data with Python
"""

import os

from .client import *  # NOQA
from .config import *  # NOQA
from .exceptions import *  # NOQA
from .json import *  # NOQA
from .utils import *  # NOQA
from .version import version as __version__  # NOQA


def _get_bibtex():
    import textwrap

    # Set the bibtex entry to the article referenced in CITATION.rst
    citation_file = os.path.join(os.path.dirname(__file__), 'CITATION.rst')

    # Explicitly specify UTF-8 encoding in case the system's default encoding is problematic
    with open(citation_file, encoding='utf-8') as citation:
        # Extract the first bibtex block:
        ref = citation.read().partition('.. code:: bibtex\n\n')[2]
        lines = ref.split('\n')
        # Only read the lines which are indented
        lines = lines[: [line.startswith('    ') for line in lines].index(False)]
        ref = textwrap.dedent('\n'.join(lines))
    return ref


__citation__ = __bibtex__ = _get_bibtex()
