====
drms
====

`Docs <https://docs.sunpy.org/projects/drms>`_ |
`Tutorial <https://docs.sunpy.org/projects/drms/en/latest/tutorial.html>`_ |
`Github <https://github.com/sunpy/drms>`_ |
`PyPI <https://pypi.python.org/pypi/drms>`_ 

|JOSS| |Zenodo|

.. |JOSS| image:: https://joss.theoj.org/papers/10.21105/joss.01614/status.svg
   :target: https://doi.org/10.21105/joss.01614
.. |Zenodo| image:: https://zenodo.org/badge/58651845.svg
   :target: https://zenodo.org/badge/latestdoi/58651845

The ``drms`` module provides an easy-to-use interface for accessing HMI,
AIA and MDI data with Python. It uses the publicly accessible
`JSOC <http://jsoc.stanford.edu/>`_ DRMS server by default, but can also
be used with local `NetDRMS <http://jsoc.stanford.edu/netdrms/>`_ sites.
More information, including a detailed tutorial, is available in the
`Documentation <https://docs.sunpy.org/projects/drms>`_.


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

If you are using `Anaconda`_, it is recommended to use the `conda-forge`_
package::

    conda config --append channels conda-forge
    conda install drms

Otherwise the ``drms`` Python package can be installed from `PyPI`_ using

::

    pip install drms

Note: If you do not use a Python distribution, like `Anaconda`_,
and did not create an isolated Python environment using `Virtualenv`_,
you might need to add ``--user`` to the ``pip`` command::

    pip install --user drms


.. _PyPI: https://pypi.python.org/pypi/drms
.. _conda-forge: https://anaconda.org/conda-forge/drms
.. _Anaconda: https://www.anaconda.com/distribution/
.. _Virtualenv: https://virtualenv.pypa.io


Running Tests
-------------

In order to run any unit tests, `pytest`_ needs to be installed.

Basic tests for the currently installed ``drms`` package can be run using::

    python -m drms.tests

To perform online tests against the JSOC servers, use the ``--run-jsoc`` flag::

    python -m drms.tests --run-jsoc

To also include additional email verification and JSOC export tests,
you need to specify a `registered email address`_, e.g.::

    python -m drms.tests --run-jsoc --email name@example.com

.. _pytest: https://pypi.org/project/pytest/
.. _registered email address: http://jsoc.stanford.edu/ajax/register_email.html


Getting Help
------------

This is a SunPy-affiliated package. For more information or to ask questions
about drms or SunPy, check out:

-  `drms Documentation`_
-  `SunPy Matrix Channel`_
-  `SunPy Mailing List`_

.. _drms Documentation: https://docs.sunpy.org/projects/drms/en/latest/
.. _SunPy Matrix Channel: https://riot.im/app/#/room/#sunpy:matrix.org
.. _SunPy Mailing List: https://groups.google.com/forum/#!forum/sunpy


Contributing
------------

If you would like to get involved, start by joining the `SunPy mailing list`_
and check out the `Developers Guide`_ section of the SunPy docs. Stop by our
chat room `#sunpy:matrix.org`_ if you have any questions.
Help is always welcome so let us know what you like to work on, or check out
the `issues page`_ for the list of known outstanding items.

For more information on contributing to SunPy, please read our
`Newcomers' guide`_.

.. _SunPy mailing list: https://groups.google.com/forum/#!forum/sunpy
.. _Developers Guide: https://docs.sunpy.org/en/latest/dev_guide/index.html
.. _`#sunpy:matrix.org`: https://riot.im/app/#/room/#sunpy:matrix.org
.. _issues page: https://github.com/sunpy/drms/issues
.. _Newcomers' guide: https://docs.sunpy.org/en/latest/dev_guide/newcomers.html


Code of Conduct
---------------

When you are interacting with the SunPy community you are asked to follow
our `Code of Conduct`_.

.. _Code of Conduct: https://docs.sunpy.org/en/latest/code_of_conduct.html


Acknowledgements
----------------

The main author of this project has received funding from the European
Research Council under the European Union's Seventh Framework Programme
(FP/2007-2013) / ERC Grant Agreement no. 307117.

Parts of this file were adopted from the SunPy README file,
Copyright (c) 2013-2019 The SunPy developers.

See AUTHORS.txt for a list of contributors.
