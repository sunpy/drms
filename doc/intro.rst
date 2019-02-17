Introduction
============

The ``drms`` Python package can be used to access HMI, AIA and MDI data
which are stored in a DRMS database system.

DRMS stands for *Data Record Management System* and is a system that was
developed by the
`Joint Science Operation Center <http://jsoc.stanford.edu/>`_
(JSOC), headquartered at Stanford University, to handle the data produced
by the AIA and HMI instruments aboard the
`Solar Dynamics Observatory <http://sdo.gsfc.nasa.gov/>`_
spacecraft.

By default the ``drms`` module uses the HTTP/JSON interface provided by
JSOC and has similar functionality to the
`JSOC Lookdata <http://jsoc.stanford.edu/ajax/lookdata.html>`_
website. It can be used to query metadata, submit data export requests
and download data files.

This module also works well for local
`NetDRMS <http://jsoc.stanford.edu/netdrms/>`_
sites, as long as the site runs a web server providing the needed CGI
programs ``show_series`` and ``jsoc_info`` (for the data export
functionality, additional CGIs, like ``jsoc_fetch``, are needed).


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


.. note::
   If you do not use a Python distribution, like
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

See :download:`LICENSE.txt <../LICENSE.txt>` for the license text and
:download:`AUTHORS.txt <../AUTHORS.txt>` for a list of contributors.
