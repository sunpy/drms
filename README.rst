====
drms
====

`Docs <http://drms.readthedocs.io/>`_ |
`Tutorial <http://drms.readthedocs.io/en/stable/tutorial.html>`_ |
`Github <https://github.com/kbg/drms>`_ |
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
-  Pandas, version 0.14.1 or newer
-  Six, version 1.8.0 or newer

The module might also work with earlier versions, but it has not been
tested with any versions older than the ones listed above.


Installation
------------

The ``drms`` Python package can be installed from
`PyPI <https://pypi.python.org/pypi/drms>`_ using

::

    pip install --user drms

To upgrade an already existing installation to the latest version, you
can write

::

    pip install -U --user drms

The ``--user`` argument can be omitted in the ``pip`` command, if you are
using a Python distribution, like
`Anaconda <https://www.continuum.io/downloads>`_,
or if you created an isolated Python environment using
`Virtualenv <https://virtualenv.pypa.io/en/stable/>`_.


Acknowledgements
----------------

The author of this project has received funding from the European
Research Council under the European Union's Seventh Framework Programme
(FP/2007-2013) / ERC Grant Agreement no. 307117.

Some of the data export code was contributed by Monica Bobra and Art
Amezcua.
