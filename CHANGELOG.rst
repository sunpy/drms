0.6.4 (2023-06-09)
==================

Bug Fixes
---------

- Modified :meth:`drms.client.Client._convert_numeric_keywords` to use a row-centric approach for handling hexadecimal strings. (`#102 <https://github.com/sunpy/drms/pull/102>`__)
- Modified :meth:`drms.utils.to_datetime` to work with Pandas 2.0. (`#103 <https://github.com/sunpy/drms/pull/102>`__)
- Fixed pandas 2.0.0 warning.  (`#97 <https://github.com/sunpy/drms/pull/97>`__)


0.6.3 (2022-10-13)
==================

Bug Fixes
---------

- Updated indexing in a function to prevent FutureWarnings from pandas. (`#73 <https://github.com/sunpy/drms/pull/73>`__)


Trivial/Internal Changes
------------------------

- Updated the init of `drms.json.HttpJsonRequest` to raise a nicer message if the URL fails to open. (`#76 <https://github.com/sunpy/drms/pull/76>`__)


0.6.2 (2021-05-15)
==================

Trivial
-------

- Tidy up of internal code that has no user facing changes.


0.6.1 (2021-01-23)
==================

Bug Fixes
---------

- Fixed issue with downloads not having the primekeys substituted with their correct values in downloaded filenames. (`#52 <https://github.com/sunpy/drms/pull/52>`__)


0.6.0 (2020-11-01)
==================

Improved Documentation
----------------------

- Examples has been formatted into an online gallery.

Backwards Incompatible Changes
------------------------------

- Python 2 support has been dropped, only Python 3.7 or higher is supported.

Deprecations and Removals
-------------------------

- ``Client.get()`` has been removed, use :meth:`drms.client.Client.query()` instead.

Support for Processing Keywords
--------------------------------

- :meth:`drms.client.Client.export` now accepts a ``process`` keyword argument
- This allows users to specify additional server-side processing options such as image cutouts
- See the "Processing" section of the `JSOC Data Export page <http://jsoc.stanford.edu/ajax/exportdata.html>`__ for more information.
