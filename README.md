drms_json
=========

The `drms_json.py` module provides an easy way to access HMI, MDI and AIA data with Python, using the JSON web interface provided by [JSOC](http://jsoc.stanford.edu/). It has the same functionality as the [JSOC Lookdata](http://jsoc.stanford.edu/ajax/lookdata.html) website.

The module also works well for local [NetDRMS](http://jsoc.stanford.edu/netdrms/) sites, as long as the site runs a web server providing the needed CGI programs `show_series` and `jsoc_info`.


Requirements
------------

The module supports Python 2.7 and Python 3.4 or newer. It requires the following Python packages:

- NumPy, version 1.9.0 or newer
- Pandas, version 0.14.1 or newer
- Six, version 1.8.0 or newer

The module might also work with earlier versions, but it has not been tested with any versions older than the ones listed above.


Installation
------------

Just copy or symlink the file `drms_json.py` to any directory where you want to use it.

Alternatively you can also use the provided `setup.py` script to install it to your user's Python path:

    python setup.py install --user

If you use `setup.py`, you need to run this script with the same Python version, you want to use `drms_json.py` with. If you, for example, want to use it from Python 2 as well as from Python 3, then you need to run `setup.py` twice, once with the `python2` binary and once with `python3` (or however those binaries are called on your system).


How to use
----------

All you need to do is to import the `drms_json` module and create a `Client` instance:

    import drms_json as drms
    c = drms.Client()

After this, you can obtain a list of all available data series using the `c.series()` method, get a list of keywords or primekeys of a certain series using `c.keys()` or `c.pkeys()` respectively, or get even more information on a series using the `c.info()` method. Record set queries for retrieving keyword data or locations of data segments can be performed by using the method `c.get()`. TAI time strings can be converted into a (naive) Python representation, by using the utility function `drms.to_datetime()`. Data keywords and segments are bound together, exported as fits files, and served at jsoc.stanford.edu using the `c.export()` method.

For more information, use `help(drms.Client)` inside the Python interpreter and have a look at the provided examples.


Acknowledgements
----------------

The author of this project has received funding from the European Research Council under the European Union's Seventh Framework Programme (FP/2007-2013) / ERC Grant Agreement no. 307117.

The `c.export()` method was written by Monica Bobra and Art Amezcua.
