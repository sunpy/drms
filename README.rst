====
drms
====

`Docs <http://drms.readthedocs.io/>`_ |
`Tutorial <https://drms.readthedocs.io/en/latest/tutorial.html>`_ |
`Github <https://github.com/sunpy/drms>`_ |
`PyPI <https://pypi.python.org/pypi/drms>`_

The ``drms`` module provides an easy-to-use interface for accessing HMI,
AIA and MDI data with Python. It uses the publicly accessible
`JSOC <http://jsoc.stanford.edu/>`_ DRMS server by default, but can also
be used with local `NetDRMS <http://jsoc.stanford.edu/netdrms/>`_ sites.
More information, including a detailed tutorial is available on
`Read the Docs <http://drms.readthedocs.io/>`_.


Requirements
------------

The ``drms`` module supports Python 2.7 and Python 3.4 or newer. It
requires the following Python packages:

-  NumPy, version 1.9.0 or newer
-  Pandas, version 0.15.0 or newer
-  Six, version 1.8.0 or newer

The module might also work with earlier versions, but it has not been
tested with any versions older than the ones listed above.


Installation
------------

The ``drms`` Python package can be installed from
`PyPI <https://pypi.python.org/pypi/drms>`_ using

::

    pip install drms

To upgrade an already existing installation to the latest release, you
can write::

    pip install -U drms


Note: If you do not use a Python distribution, like
`Anaconda <https://www.continuum.io/downloads>`_,
and did not create an isolated Python environment using
`Virtualenv <https://virtualenv.pypa.io/en/stable/>`_,
you might need to add ``--user`` to the ``pip`` command::

    pip install --user drms


Acknowledgements
----------------

The main author of this project has received funding from the European
Research Council under the European Union's Seventh Framework Programme
(FP/2007-2013) / ERC Grant Agreement no. 307117.

See AUTHORS.txt for a list of contributors.
