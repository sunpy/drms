Introduction
============

The ``drms`` Python package can be used to access HMI, AIA and MDI data which are stored in a DRMS database system.

DRMS stands for *Data Record Management System* and is a system that was developed by the `Joint Science Operation Center <http://jsoc.stanford.edu/>`__ (JSOC), headquartered at Stanford University, to handle the data produced by the AIA and HMI instruments aboard the `Solar Dynamics Observatory <http://sdo.gsfc.nasa.gov/>`__ spacecraft.

By default the ``drms`` library uses the HTTP/JSON interface provided by JSOC and has similar functionality to the `JSOC Lookdata <http://jsoc.stanford.edu/ajax/lookdata.html>`__ website.
It can be used to query metadata, submit data export requests and download data files.

This module also works well for local `NetDRMS <http://jsoc.stanford.edu/netdrms/>`__ sites, as long as the site runs a web server providing the needed CGI programs ``show_series`` and ``jsoc_info`` (for the data export functionality, additional CGIs, like ``jsoc_fetch``, are needed).

Requirements
------------

The ``drms`` module supports Python 3.7 or newer.
It requires the following Python packages:

-  numpy
-  pandas

Installation
------------

If you are using `Anaconda`_, it is recommended to use the `conda-forge`_ package::

    conda config --append channels conda-forge
    conda install drms

Otherwise the ``drms`` Python package can be installed from `PyPI`_ using::

    pip install drms

.. note::
   If you do not use a Python distribution, like `Anaconda`_,
   and did not create an isolated Python environment using `Virtualenv`_,
   you might need to add ``--user`` to the ``pip`` command::

       pip install --user drms

.. _PyPI: https://pypi.python.org/pypi/drms
.. _conda-forge: https://anaconda.org/conda-forge/drms
.. _Anaconda: https://www.anaconda.com/distribution/
.. _Virtualenv: https://virtualenv.pypa.io

Acknowledgements
----------------

Kolja Glogowski has received funding from the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117.
