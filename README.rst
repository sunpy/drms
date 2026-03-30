``drms``
========

Access HMI, AIA and MDI data from the Standford JSOC DRMS

`Docs <https://docs.sunpy.org/projects/drms/>`__ |
`Tutorial <https://docs.sunpy.org/projects/drms/en/latest/tutorial.html>`__ |
`Github <https://github.com/sunpy/drms>`__ |
`PyPI <https://pypi.org/project/drms/>`__

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

For more information or to ask questions about ``drms``, check out:

- `drms Documentation <https://docs.sunpy.org/projects/drms/en/latest/>`__
- `SunPy Chat <https://app.element.io/#/room/#sunpy:openastronomy.org>`__

Usage of Generative AI
----------------------

We expect authentic engagement in our community.
**Do not post the output from Large Language Models or similar generative AI as code, issues or comments on GitHub or any other platform.**
If you use generative AI tools as an aid in developing code or documentation changes, ensure that you fully understand the proposed changes and can explain why they are the correct approach and an improvement to the current state.
For more information see our documentation on fair and appropriate `AI usage <https://docs.sunpy.org/en/latest/dev_guide/contents/ai_usage.html>`__.

Contributing
------------

We love contributions! drms is open source,
built on open source, and we'd love to have you hang out in our community.

If you would like to get involved, check out the `Developers Guide`_ section of the SunPy docs.
Stop by our chat room `#sunpy:openastronomy.org`_ if you have any questions.
Help is always welcome so let us know what you like to work on, or check out the `issues page`_ for the list of known outstanding items.

For more information on contributing to SunPy, please read our `Newcomers' guide`_.

.. _Developers Guide: https://docs.sunpy.org/en/latest/dev_guide/index.html
.. _`#sunpy:openastronomy.org`: https://app.element.io/#/room/#sunpy:openastronomy.org
.. _issues page: https://github.com/sunpy/drms/issues
.. _Newcomers' guide: https://docs.sunpy.org/en/latest/dev_guide/contents/newcomers.html

When you are interacting with the SunPy community you are asked at to follow our `code of conduct <https://sunpy.org/coc>`__.

Citation
--------
If you use ``drms`` in your work, please cite our `paper <https://doi.org/10.21105/joss.01614>`__.

.. code-block:: bibtex

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

Acknowledgements
----------------

Kolja Glogowski has received funding from the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117.
