====
drms
====

`Docs <https://docs.sunpy.org/projects/drms/>`__ |
`Tutorial <https://docs.sunpy.org/projects/drms/en/latest/tutorial.html>`__ |
`Github <https://github.com/sunpy/drms>`__ |
`PyPI <https://pypi.python.org/pypi/drms>`__

|JOSS| |Zenodo|

.. |JOSS| image:: https://joss.theoj.org/papers/10.21105/joss.01614/status.svg
   :target: https://doi.org/10.21105/joss.01614
.. |Zenodo| image:: https://zenodo.org/badge/58651845.svg
   :target: https://zenodo.org/badge/latestdoi/58651845

The ``drms`` module provides an easy-to-use interface for accessing HMI, AIA and MDI data with Python.
It uses the publicly accessible `JSOC <http://jsoc.stanford.edu/>`__ DRMS server by default, but can also be used with local `NetDRMS <http://jsoc.stanford.edu/netdrms/>`__ sites.
More information, including a detailed tutorial, is available in the `Documentation <https://docs.sunpy.org/projects/drms/>`__.

Getting Help
------------

This is a SunPy-affiliated package. For more information or to ask questions
about drms or SunPy, check out:

-  `drms Documentation`_
-  `SunPy Matrix Channel`_
-  `SunPy mailing list`_

.. _drms Documentation: https://docs.sunpy.org/projects/drms/en/latest/
.. _SunPy Matrix Channel: https://riot.im/app/#/room/#sunpy:matrix.org

Contributing
------------

If you would like to get involved, start by joining the `SunPy mailing list`_ and check out the `Developers Guide`_ section of the SunPy docs.
Stop by our chat room `#sunpy:matrix.org`_ if you have any questions.
Help is always welcome so let us know what you like to work on, or check out the `issues page`_ for the list of known outstanding items.

For more information on contributing to SunPy and to DRMS, please read our `Newcomers guide`_.

.. _SunPy mailing list: https://groups.google.com/forum/#!forum/sunpy
.. _Developers Guide: https://docs.sunpy.org/en/latest/dev_guide/index.html
.. _`#sunpy:matrix.org`: https://app.element.io/#/room/#sunpy:openastronomy.org
.. _issues page: https://github.com/sunpy/drms/issues
.. _Newcomers guide: https://docs.sunpy.org/en/latest/dev_guide/newcomers.html

Code of Conduct (CoC)
---------------------

When you are interacting with the SunPy community you are asked to follow our `code of conduct`_.

.. _code of conduct: https://docs.sunpy.org/en/latest/code_of_conduct.html

Citation
--------

If you use ``drms`` in your work, please consider citing our `paper`_.

.. code :: bibtex

    @article{Glogowski2019,
      doi = {10.21105/joss.01614},
      url = {https://doi.org/10.21105/joss.01614},
      year = {2019},
      publisher = {The Open Journal},
      volume = {4},
      number = {40},
      pages = {1614},
      author = {Kolja Glogowski and Monica G. Bobra and Nitin Choudhary and Arthur B. Amezcua and Stuart J. Mumford},
      title = {drms: A Python package for accessing HMI and AIA data},
      journal = {Journal of Open Source Software}
    }

.. _paper: https://doi.org/10.21105/joss.01614

Acknowledgements
----------------

Kolja Glogowski has received funding from the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117.
