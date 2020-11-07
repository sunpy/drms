.. _tutorial:

Tutorial
========

This tutorial gives an introduction on how to use the ``drms`` Python library.
More detailed information on the different classes and functions can be found in the :ref:`API Reference <reference>`.

Basic usage
-----------

In this first part, we start with looking at data series that are available from `JSOC <http://jsoc.stanford.edu/>`__ and perform some basic DRMS queries to obtain keyword data (metadata) and segment file (data) locations.
This is essentially what you can do on the `JSOC Lookdata <http://jsoc.stanford.edu/ajax/lookdata.html>`__ website.

To be able to access the JSOC DRMS from Python, we first need to import the ``drms`` module and create an instance of the `~drms.client.Client` class::

    >>> import drms
    >>> client = drms.Client()  # doctest: +REMOTE_DATA

All available data series can be now retrieved by calling the :meth:`drms.client.Client.series` method.
HMI series names start with ``"hmi."``, AIA series names with ``"aia."`` and the names of MDI series with ``"mdi."``.

The first (optional) parameter of this method takes a regular expression that allows you to filter the result.
If you, for example, want to obtain a list of HMI series, with a name that start with the string ``"m_"``, you can write::

    >>> client.series(r'hmi\.m_')  # doctest: +REMOTE_DATA
    ['hmi.M_45s', 'hmi.M_45s_dcon', 'hmi.M_720s', 'hmi.M_720s_dcon', 'hmi.M_720s_dconS', 'hmi.m_720s_mod', 'hmi.m_720s_nrt']

Keep in mind to escape the dot character (``'.'``), like it is shown in the example above, if you want to include it in your filter string.
Also note that series names are handled in a case-insensitive way.

DRMS records can be selected by creating a query string that contains a series name, followed by one or more fields, which are surrounded by square brackets.
Each of those fields corresponds to a specific primekey, that is specified in the series definition.
A complete set of primekeys represents a unique identifier for a record in that particular series.
For more detailed information on building record set queries, including additional non-primekey fields, see the `JSOC Help <http://jsoc.stanford.edu/ajax/RecordSetHelp.html>`__ page about this topiclient.

With the ``drms`` module you can use the :meth:`drms.client.Client.pkeys` method to obtain a list of all primekeys of a series, e.g.::

    >>> client.pkeys('hmi.m_720s')  # doctest: +REMOTE_DATA
    ['T_REC', 'CAMERA']

    >>> client.pkeys('hmi.v_sht_modes')  # doctest: +REMOTE_DATA
    ['T_START', 'LMIN', 'LMAX', 'NDT']

A list of all (regular) keywords can be obtained using :meth:`drms.client.Client.keys`.
You can also use the method :meth:`drms.client.Client.info` to get more detailed information about a series, e.g.::

    >>> si = client.info('hmi.v_avg120')  # doctest: +REMOTE_DATA
    >>> si.segments  # doctest: +REMOTE_DATA
            type  units protocol       dims               note
    name
    mean   short    m/s     fits  4096x4096       Doppler mean
    power  short  m2/s2     fits  4096x4096      Doppler power
    valid  short     NA     fits  4096x4096  valid pixel count
    Log     char     NA  generic                       run log

All table-like structures, returned by routines in the ``drms`` module, are `Pandas DataFrames <http://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html>`__.
If you are new to `Pandas <http://pandas.pydata.org/>`__, you should have a look at the introduction to `Pandas Data Structures <http://pandas.pydata.org/pandas-docs/stable/dsintro.html>`__.

Record set queries, used to obtain keyword data and get the location of data segments, can be performed using the :meth:`drms.client.Client.query` method.
To get, for example, the record time and the mean value for some of the HMI Dopplergrams that were recorded on April 1, 2016, together with the spacecraft's radial velocity in respect to the Sun, you can write::

    >>> k = client.query('hmi.v_45s[2016.04.01_TAI/1d@6h]',
    ...             key='T_REC, DATAMEAN, OBS_VR')  # doctest: +REMOTE_DATA
    >>> k  # doctest: +REMOTE_DATA
                         T_REC     DATAMEAN       OBS_VR
    0  2016.04.01_00:00:00_TAI  3313.104980  3309.268006
    1  2016.04.01_06:00:00_TAI   878.075195   887.864139
    2  2016.04.01_12:00:00_TAI -2289.062500 -2284.690263
    3  2016.04.01_18:00:00_TAI   128.609283   137.836168

JSOC time strings can be converted to a naive ``datetime``
representation using the :meth:`drms.utils.to_datetime` utility function::

    >>> t = drms.to_datetime(k.T_REC)  # doctest: +REMOTE_DATA
    >>> t  # doctest: +REMOTE_DATA
    0   2016-04-01 00:00:00
    1   2016-04-01 06:00:00
    2   2016-04-01 12:00:00
    3   2016-04-01 18:00:00
    Name: T_REC, dtype: datetime64[ns]

For most of the HMI and MDI data sets, the `TAI <https://en.wikipedia.org/wiki/International_Atomic_Time>`__ time standard is used which, in contrast to `UTC <https://en.wikipedia.org/wiki/Coordinated_Universal_Time>`__, does not make use of any leap seconds.
The TAI standard is currently not supported by the Python standard libraries.
If you need to convert timestamps between TAI and UTC, you can use the `Astropy <http://www.astropy.org/>`__ time module::

    >>> from astropy.time import Time
    >>> ta = Time(t[0], format='datetime', scale='tai')  # doctest: +REMOTE_DATA
    >>> ta  # doctest: +REMOTE_DATA
    <Time object: scale='tai' format='datetime' value=2016-04-01 00:00:00>
    >>> ta.utc  # doctest: +REMOTE_DATA
    <Time object: scale='utc' format='datetime' value=2016-03-31 23:59:24>

The ``"hmi.v_45s"`` series has a data segment with the name ``"Dopplergram"``, which contains Dopplergrams for each record in the series, that are stored as `FITS <http://fits.gsfclient.nasa.gov/>`__ files.
The location of the FITS files for the record set query in the example above, can be obtained by using the ``seg`` parameter of the :meth:`drms.client.Client.query` method::

    >>> s = client.query('hmi.v_45s[2016.04.01_TAI/1d@6h]', seg='Dopplergram')  # doctest: +REMOTE_DATA
    >>> s  # doctest: +REMOTE_DATA
                                     Dopplergram
    0  /SUM58/D803708321/S00008/Dopplergram.fits
    1  /SUM41/D803708361/S00008/Dopplergram.fits
    2  /SUM71/D803720859/S00008/Dopplergram.fits
    3  /SUM70/D803730119/S00008/Dopplergram.fits

Note that the ``key`` and ``seg`` parameters can also be used together in one :meth:`drms.client.Client.query` call, i.e.::

    >>> k, s = client.query('hmi.v_45s[2016.04.01_TAI/1d@6h]',
    ...                key='T_REC, DATAMEAN, OBS_VR', seg='Dopplergram')  # doctest: +REMOTE_DATA

The file paths listed above are the storage location on the JSOC server.
You can access these files, even if you do not have direct NFS access to the filesystem, by prepending the JSOC URL to segment file path::

    >>> url = 'http://jsoc.stanford.edu' + s.Dopplergram[0]  # doctest: +REMOTE_DATA
    >>> url  # doctest: +REMOTE_DATA
    'http://jsoc.stanford.edu/SUM58/D803708321/S00008/Dopplergram.fits'

    >>> from astropy.io import fits
    >>> a = fits.getdata(url)  # doctest: +REMOTE_DATA
    >>> print(a.shape, a.dtype)  # doctest: +REMOTE_DATA
    (4096, 4096) float32

Note that FITS files which are accessed in this way, do not contain anykeyword data in their headers.
This is perfectly fine in many cases, because you can just use :meth:`drms.client.Client.query` to obtain the data of all required keywords.
If you need FITS files with headers that contain all the keyword data, you need to submit an export request to JSOC, which is described in the next section.

Export requests can also be useful, if you want to download more than only one or two files (even without keyword headers), because you can then use the :meth:`drms.client.ExportRequest.download` method, which takes care of creating URLs, downloading the data and (if necessary) generating suitable local filenames.

Data export requests
--------------------

Data export requests can be interactively built and submitted on the `JSOC Export Data <http://jsoc.stanford.edu/ajax/exportdata.html>`__ webpage, where you can also find more information about the different export options that are available.
Note that a registered email address is required to for submitting export requests. You can register your email address on the `JSOC email registration <http://jsoc.stanford.edu/ajax/register_email.html>`__ webpage.

It is advisable to have a closer look at the export webpage before submitting export requests using the ``drms`` library.
It is also possible to submit an export request on the webpage and then use the Python routines to query the request status and download files.

.. warning::
    Please replace the email below with your own registered email.

First, we start again with importing the ``drms`` library and creating a `~drms.client.Client` instance::

    >>> import drms
    >>> client = drms.Client(email='nabil.freij@gmail.com', verbose=True)  # doctest: +REMOTE_DATA

In this case we also provide an email address (which needs to be already registered at JSOC) and turn on status messages by enabling the ``verbose`` flag.

We now create a download directory for our downloads, in case it does not exist yet::

    >>> import os
    >>> out_dir = 'downloads'
    >>> if not os.path.exists(out_dir):
    ...     os.mkdir(out_dir)

Data export requests can be submitted using :meth:`drms.client.Client.export`.
The most important parameters of this method, besides the export query string, are the parameters ``method`` and ``protocol``.
There are many different export methods and protocols available.
In the following examples we confine ourselves to the methods ``url_quick`` and ``url`` and the protocols ``as-is`` and ``fits``.

url_quick / as-is
~~~~~~~~~~~~~~~~~

The most direct and quickest way of downloading files is the combination ``url_quick`` / ``as-is``.
This (in most cases) does not create an actual export request, where you would have to wait for it being finished, but rather compiles a list of files from your data export query, which can then be directly downloaded.
This also means that this kind of export usually has no ``ExportID`` assigned to it.
The only time it is treated as a "real" export request (including an ``ExportID`` and some wait time) is, when the requested data segments are not entirely online, and parts of the requested files need to be restored from tape drives.

As an example, we now create an ``url_quick`` / ``as-is`` export request for the same record set that was used in the previous section.
For export requests, the segment name is specified using an additional field in the query string, surrounded by curly braces.
Note that :meth:`drms.client.Client.export` performs an ``url_quick`` / ``as-is`` export request by default, so you do not need to explicitly use ``method='url_quick'`` and ``protocol='as-is'`` in this case::

    >>> r = client.export('hmi.v_45s[2016.04.01_TAI/1d@6h]{Dopplergram}')  # doctest: +REMOTE_DATA
    >>> r  # doctest: +REMOTE_DATA
    <ExportRequest: id=None, status=0>

    >>> r.data.filename  # doctest: +REMOTE_DATA
    0    /SUM58/D803708321/S00008/Dopplergram.fits
    1    /SUM41/D803708361/S00008/Dopplergram.fits
    2    /SUM71/D803720859/S00008/Dopplergram.fits
    3    /SUM70/D803730119/S00008/Dopplergram.fits
    Name: filename, dtype: object

Download URLs can now be generated using the :attr:`drms.client.ExportRequest.urls` attribute::

    >>> r.urls.url[0]  # doctest: +REMOTE_DATA
    'http://jsoc.stanford.edu/SUM58/D803708321/S00008/Dopplergram.fits'

Files can be downloaded using the :meth:`drms.client.ExportRequest.download` method.
You can (optionally) select which file(s) you want to download, by using the ``index`` parameter of this method. The following, for example, only downloads the first file of the request::

    >>> r.download(out_dir, 0)  # doctest: +REMOTE_DATA
    Downloading file 1 of 1...
        record: hmi.V_45s[2016.04.01_00:00:00_TAI][2]{Dopplergram}
      filename: Dopplergram.fits
      -> downloads/hmi.v_45s.20160401_000000_TAI.2.Dopplergram.fits
    ...

Being a direct ``as-is`` export, there are no keyword data written to any FITS headers.
If you need keyword data added to the headers, you have to use the ``fits`` export protocol instead, which is described below.

url / fits
~~~~~~~~~~

Using the ``fits`` export protocol, allows you to request FITS files that include all keyword data in their headers.
Note that this protocol *does not convert* other file formats into the FITS format.
The only purpose of ``protocol='fits'`` is to add keyword data to headers of segment files, that are already stored using the FITS format.

In contrast to ``url_quick`` / ``as-is`` exports, described in the previous subsection, ``url`` / ``fits`` exports always create a "real" data export request on the server, which needs to be processed before you can download the requested files.
For each request you will get an unique ``ExportID``, which can be accessed using the :attr:`drms.client.ExportRequest.id` attribute.
In addition you will get an email notification (including the ``ExportID``), which is sent to your registered email address when the requested files are ready for download.

In the following example, we use the ``hmi.sharp_720s`` series, which contains `Spaceweather HMI Active Region Patches <http://jsoc.stanford.edu/doc/data/hmi/sharp/sharp.htm>`__ (SHARPs), and download some data files from this series.

First we have a look at the content of the series, by using :meth:`drms.client.Client.info` to get a `~drms.client.SeriesInfo` instance for this particular series::

    >>> si = client.info('hmi.sharp_720s')  # doctest: +REMOTE_DATA

    >>> si.note  # doctest: +REMOTE_DATA
    'Spaceweather HMI Active Region Patch (SHARP): CCD coordinates'

    >>> si.primekeys  # doctest: +REMOTE_DATA
    ['HARPNUM', 'T_REC']

This series contains a total of 31 different data segments::

    >>> len(si.segments)  # doctest: +REMOTE_DATA
    31

    >>> si.segments.index.values  # doctest: +REMOTE_DATA
    array(['magnetogram', 'bitmap', 'Dopplergram', 'continuum', 'inclination',
           'azimuth', 'field', 'vlos_mag', 'dop_width', 'eta_0', 'damping',
           'src_continuum', 'src_grad', 'alpha_mag', 'chisq', 'conv_flag',
           'info_map', 'confid_map', 'inclination_err', 'azimuth_err',
           'field_err', 'vlos_err', 'alpha_err', 'field_inclination_err',
           'field_az_err', 'inclin_azimuth_err', 'field_alpha_err',
           'inclination_alpha_err', 'azimuth_alpha_err', 'disambig',
           'conf_disambig'], dtype=object)

Here, we are only interested in magnetograms and continuum intensity maps ::

    >>> si.segments.loc[['continuum', 'magnetogram']]  # doctest: +REMOTE_DATA
                type  units protocol     dims                 note
    name
    continuum    int   DN/s     fits  VARxVAR  continuum intensity
    magnetogram  int  Gauss     fits  VARxVAR          magnetogram

which are stored as FITS files with varying dimensions.

If we now want to submit an export request for a magnetogram and an intensity map of HARP number 4864, recorded at midnight on November 30, 2014, we can use the following export query string::

    >>> ds = 'hmi.sharp_720s[4864][2014.11.30_00:00_TAI]{continuum, magnetogram}'  # doctest: +REMOTE_DATA

In order to obtain FITS files that include keyword data in their headers, we then need to use ``protocol='fits'`` when submitting the request using :meth:`drms.client.Client.export`::

    >>> r = client.export(ds, method='url', protocol='fits')  # doctest: +REMOTE_DATA
    >>> r  # doctest: +REMOTE_DATA
    <ExportRequest: id=JSOC_..., status=2>

We now need to wait for the server to prepare the requested files::

    >>> r.wait()  # doctest: +REMOTE_DATA
    Export request pending. [id=..., status=2]
    Waiting for 5 seconds...
    ...

    >>> r.status  # doctest: +REMOTE_DATA
    0

Note that calling :meth:`drms.client.ExportRequest.wait` is optional.
It gives you some control over the waiting process, but it can be usually omitted, in which case :meth:`~drms.client.ExportRequest.wait` is called implicitly, when you for example try to download the requested files.

After the export request is finished, a unique request URL is created for you, which points to the location where all your requested files are stored.
You can use the :attr:`drms.client.ExportRequest.request_url` attribute to obtain this URL::

    >>> r.request_url  # doctest: +REMOTE_DATA
    'http://jsoc.stanford.edu/.../S00000'

Note that this location is only temporary and that all files will be deleted after a couple of days.

Downloading the data works exactly like in the previous example, by using the :meth:`drms.client.ExportRequest.download` method::

    >>> r.download(out_dir)  # doctest: +REMOTE_DATA
    Downloading file 1 of 2...
    ...
    Downloading file 2 of 2...
    ...

.. note::
   If you want to access an existing export request that you have submitted earlier, or if you submitted an export request using the `JSOC Export Data <http://jsoc.stanford.edu/ajax/exportdata.html>`__ webpage and want to access it from Python, you can use the :meth:`drms.client.Client.export_from_id` method with the corresponding ``ExportID`` to create an `drms.client.ExportRequest` instance for this particular request.
