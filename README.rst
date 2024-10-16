====
drms
====

Access HMI, AIA and MDI data from the Standford JSOC DRMS.

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

License
-------

This project is Copyright (c) The SunPy Community and licensed under
the terms of the BSD 2-Clause license. This package is based upon
the `Openastronomy packaging guide <https://github.com/OpenAstronomy/packaging-guide>`_
which is licensed under the BSD 3-clause licence. See the licenses folder for
more information.

Contributing
------------

We love contributions! drms is open source,
built on open source, and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not
ready to be an open source contributor; that your skills aren't nearly good
enough to contribute. What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong. If you can write code at
all, you can contribute code to open source. Contributing to open source
projects is a fantastic way to advance one's coding skills. Writing perfect code
isn't the measure of a good developer (that would disqualify all of us!); it's
trying to create something, making mistakes, and learning from those
mistakes. That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either. You can
help out by writing documentation, tests, or even giving feedback about the
project (and yes - that includes giving feedback about the contribution
process). Some of these contributions may be the most valuable to the project as
a whole, because you're coming to the project with fresh eyes, so you can see
the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by
`Adrienne Lowe <https://github.com/adriennefriend>`_ for a
`PyCon talk <https://www.youtube.com/watch?v=6Uj746j9Heo>`_, and was adapted by
drms based on its use in the README file for the
`MetPy project <https://github.com/Unidata/MetPy>`_.

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

Code of Conduct (CoC)
---------------------

When you are interacting with the SunPy community you are asked to follow our `code of conduct <https://docs.sunpy.org/en/latest/code_of_conduct.html>`__.

Acknowledgements
----------------

Kolja Glogowski has received funding from the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117.
