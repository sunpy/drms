Acknowledging or Citing drms
============================

If you use drms in your scientific work, we would appreciate citing it in your publications.
The continued growth and development of drms is dependent on the community being aware of drms.

Please add the following line within your methods, conclusion or acknowledgements sections:

   *This research used version X.Y.Z (software citation) of the drms open source software package (project citation).*

The project citation should be to the `drms paper`_, and the software citation should be the specific `Zenodo DOI`_ for the version used in your work.

Here is the Bibtex entry:

.. code:: bibtex

    @ARTICLE{Glogowski2019,
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

You can also get this information with ``drms.__citation__``.

Or as, "Glogowski et al., (2019). drms: A Python package for accessing HMI and AIA data. Journal of Open Source Software, 4(40), 1614, https://doi.org/10.21105/joss.01614."

.. _drms paper: https://doi.org/10.21105/joss.01614
.. _Zenodo DOI: https://doi.org/10.5281/zenodo.3369966
