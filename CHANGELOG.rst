0.7.1 (2023-12-28)
==================

Bug Fixes
---------

- Incorrect setup of the logger is now fixed. (`#113 <https://github.com/sunpy/drms/pull/113>`__)
- Fixed missing environment variable in the docs. (`#113 <https://github.com/sunpy/drms/pull/113>`__)

0.7.0 (2023-11-17)
==================

Backwards Incompatible Changes
------------------------------

- Dropped Python 3.8 support. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- Updated all of the sphinx anchors to be more consistent.
  This means that any use of the old anchors (intersphinx links to sunpy doc pages) will need to be updated. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- Removed ``verbose`` keyword argument from `drms.Client`.
  Now all prints are done via the logging module. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- ``drms.const`` was renamed to `drms.JsocInfoConstants`
  It is also now a `Enum`. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- Renamed keywords or arguments from ``requestor`` to ``requester``. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- Removed ``debug`` keyword argument from `drms.HttpJsonClient`
  Now all prints are done via the logging module. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- Removed all FTP options. (`#90 <https://github.com/sunpy/drms/pull/90>`__)
- All keywords have to be passed by reference, no more positional keywords arguments are allowed. (`#90 <https://github.com/sunpy/drms/pull/90>`__)


Trivial/Internal Changes
------------------------

- Added "ruff" to the pre-commit and fixed the errors. (`#90 <https://github.com/sunpy/drms/pull/90>`__)


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
