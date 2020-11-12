drms v0.6.0 (2020-11-01)
========================

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
