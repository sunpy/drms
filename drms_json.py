# Copyright (c) 2014, 2015 Kolja Glogowski
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

from __future__ import absolute_import, division, print_function
import sys
import re
import types
import json
import six
from six.moves.urllib.request import urlopen
from six.moves.urllib.parse import urlencode, urljoin
import pandas as pd
import numpy as np


__all__ = ['JsonClient', 'Client', 'to_datetime', 'const']
__author__ = 'Kolja Glogowski'
__email__ = 'kolja@pixie.de'
__license__ = 'MIT'
__version__ = '0.2.1'


# Compatibility functions for older pandas versions.
if tuple(map(int, pd.__version__.split('.')[:2])) < (0, 17):
    def _pd_to_datetime_coerce(arg):
        return pd.to_datetime(arg, coerce=True)

    def _pd_to_numeric_coerce(arg):
        if not isinstance(arg, pd.Series):
            arg = pd.Series(arg)
        return arg.convert_objects(
            convert_dates=False, convert_numeric=True,
            convert_timedeltas=False)
else:
    def _pd_to_datetime_coerce(arg):
        return pd.to_datetime(arg, errors='coerce')

    def _pd_to_numeric_coerce(arg):
        return pd.to_numeric(arg, errors='coerce')


# Base URL shortcuts
_locations = {
    'jsoc': 'http://jsoc.stanford.edu/cgi-bin/ajax/',
    'kis': 'http://drms.kis.uni-freiburg.de/cgi-bin/'
}

# Set the default base URL
_locations[None] = _locations['jsoc']


# Constants for jsoc_info calls
class _JsocInfoConstants:
    all = '**ALL**'
    none = '**NONE**'
    recnum = '*recnum*'
    sunum = '*sunum*'
    size = '*size*'
    online = '*online*'
    retain = '*retain*'
    logdir = '*logdir*'
const = _JsocInfoConstants()


def _split_arg(arg):
    if isinstance(arg, six.string_types):
        arg = [it for it in re.split(r'[\s,]+', arg) if it]
    return arg


def to_datetime(tstr, force=False):
    """
    Tries to parse JSOC time strings. In general, this is quite complicated
    because of the many different (non-standard) ways they support. For more
    (much more!) details on this matter, see Rick Bogarts notes at

        http://jsoc.stanford.edu/doc/timerep.html

    Here we only try to convert the typical HMI time strings, with a format
    like %Y.%m.%d_%H:%M:%S_TAI, to an ISO time string, that can be parsed by
    pandas. Note that _TAI, aswell as other timezone indentifier like Z,
    will not be taken into account, so the result will be a naive timestamp
    without any associated timezone.

    If you know the time string format, it might be better calling
    pandas.to_datetime() directly.

    Parameters
    ----------
    tstr : string or list/Series containing strings
        DateTime strings.
    force : boolean
        Set to True to omit the endswith('_TAI') check.

    Returns
    -------
    result : Series or Timestamp
        Pandas series or a single Timestamp object
    """
    s = pd.Series(tstr)
    if force or s.str.endswith('_TAI').any():
        s = s.str.replace('_TAI', '')
        s = s.str.replace('_', ' ')
        s = s.str.replace('.', '-', n=2)
    res = _pd_to_datetime_coerce(s)
    return res.iloc[0] if isinstance(tstr, six.string_types) else res


class JsonRequest(object):
    def __init__(self, url, encoding):
        self._encoding = encoding
        self._http = urlopen(url)
        self._data_str = None
        self._data = None

    def _parse_json(self, data):
        return json.loads(data.decode(self._encoding))

    def __repr__(self):
        return '<JsonRequest "%s">' % self.url

    @property
    def url(self):
        return self._http.url

    @property
    def raw_data(self):
        if self._data_str is None:
            self._data_str = self._http.read()
        return self._data_str

    @property
    def data(self):
        if self._data is None:
            self._data = json.loads(self.raw_data.decode(self._encoding))
        return self._data


class JsonClient(object):
    def __init__(self, baseurl=None, encoding='latin1', debug=False):
        """
        Parameters
        ----------
        baseurl : string or None
            Base URL of the DRMS CGIs. Defaults to JSOC.
        encoding : string
            Character encoding. Defaults to 'latin1'
        debug : boolean
            Enable or disable debug mode. Default is disabled.
        """
        self._encoding = encoding
        self.baseurl = baseurl
        self.debug = debug

    def __repr__(self):
        return '<JsonClient "%s">' % self.baseurl

    def _json_request(self, url):
        if self.debug:
            print(url)
        return JsonRequest(url, self._encoding)

    @property
    def baseurl(self):
        return self._baseurl

    @baseurl.setter
    def baseurl(self, value):
        if value is None:
            baseurl = _locations[None]
        else:
            baseurl = _locations.get(value.lower(), None)
            if baseurl is None:
                baseurl = value
        url_show_series = urljoin(baseurl, 'show_series')
        url_jsoc_info = urljoin(baseurl, 'jsoc_info')
        self._baseurl = baseurl
        self._url_show_series = url_show_series
        self._url_jsoc_info = url_jsoc_info

    @property
    def debug(self):
        return self._debug

    @debug.setter
    def debug(self, value):
        self._debug = True if value else False

    def show_series(self, ds_filter=None):
        """
        List available data series.

        Parameters
        ----------
        ds_filter : string
            Name filter regexp.

        Returns
        -------
        result : dict
        """
        query = '?' if ds_filter is not None else ''
        if ds_filter is not None:
            query += urlencode({'filter': ds_filter})
        req = self._json_request(self._url_show_series + query)
        return req.data

    def series_struct(self, ds):
        """
        Get information about the content of a data series.

        Parameters
        ----------
        ds : string
            Name of the data series.

        Returns
        -------
        result : dict
            Dictionary containing information about the data series.
        """
        query = '?' + urlencode({'op': 'series_struct', 'ds': ds})
        req = self._json_request(self._url_jsoc_info + query)
        return req.data

    def rs_summary(self, ds):
        """
        Get summary (i.e. count) of a given record set.

        Parameters
        ----------
        ds : string
            Record set query (only one series).

        Returns
        -------
        result : dict
            Dictionary containg 'count', 'status' and 'runtime'.
        """
        query = '?' + urlencode({'op': 'rs_summary', 'ds': ds})
        req = self._json_request(self._url_jsoc_info + query)
        return req.data

    def rs_list(self, ds, key=None, seg=None, link=None, uid=None):
        """
        Get detailed information about a record set.

        Parameters
        ----------
        ds : string
            Record set query.
        key : string, list or None
            List of requested keywords, optional.
        seg : string, list or None
            List of requested segments, optional.
        link : string or None
            List of requested Links, optional.
        uid : string or None
            Session ID used when calling rs_list CGI, optional.

        Returns
        -------
        result : dict
            Dictionary containing the requested record set information.
        """
        if key is None and seg is None and link is None:
            raise ValueError('At least one key, seg or link must be specified')
        d = {'op': 'rs_list', 'ds': ds}
        if key is not None:
            d['key'] = ','.join(_split_arg(key))
        if seg is not None:
            d['seg'] = ','.join(_split_arg(seg))
        if link is not None:
            d['link'] = ','.join(_split_arg(link))
        if uid is not None:
            d['userhandle'] = uid
        query = '?' + urlencode(d)
        req = self._json_request(self._url_jsoc_info + query)
        return req.data


class SeriesInfo(object):
    def __init__(self, d, name=None):
        self.json = d
        self.name = name
        self.retention = self.json.get('retention')
        self.unitsize = self.json.get('unitsize')
        self.archive = self.json.get('archive')
        self.tapegroup = self.json.get('tapegroup')
        self.note = self.json.get('note')
        self.primekeys = self.json.get('primekeys')
        self.dbindex = self.json.get('dbindex')
        self.keywords = self._parse_keywords(d['keywords'])
        self.links = self._parse_links(d['links'])
        self.segments = self._parse_segments(d['segments'])

    @classmethod
    def _parse_keywords(cls, d):
        keys = [
            'name', 'type', 'recscope', 'defval', 'units', 'note', 'linkinfo']
        res = []
        for di in d:
            resi = []
            for k in keys:
                resi.append(di.get(k))
            res.append(tuple(resi))
        if not res:
            res = None  # workaround for older pandas versions
        res = pd.DataFrame(res, columns=keys)
        res.index = res.pop('name')
        res['is_time'] = (res.type == 'time')
        res['is_integer'] = (res.type == 'short')
        res['is_integer'] |= (res.type == 'int')
        res['is_integer'] |= (res.type == 'longlong')
        res['is_real'] = (res.type == 'float')
        res['is_real'] |= (res.type == 'double')
        res['is_numeric'] = (res.is_integer | res.is_real)
        return res

    @classmethod
    def _parse_links(cls, d):
        keys = ['name', 'target', 'kind', 'note']
        res = []
        for di in d:
            resi = []
            for k in keys:
                resi.append(di.get(k))
            res.append(tuple(resi))
        if not res:
            res = None  # workaround for older pandas versions
        res = pd.DataFrame(res, columns=keys)
        res.index = res.pop('name')
        return res

    @classmethod
    def _parse_segments(cls, d):
        keys = ['name', 'type', 'units', 'protocol', 'dims', 'note']
        res = []
        for di in d:
            resi = []
            for k in keys:
                resi.append(di.get(k))
            res.append(tuple(resi))
        if not res:
            res = None  # workaround for older pandas versions
        res = pd.DataFrame(res, columns=keys)
        res.index = res.pop('name')
        return res

    def __repr__(self):
        if self.name is None:
            return '<SeriesInfo>'
        else:
            return '<SeriesInfo "%s">' % self.name


class Client(object):
    def __init__(self, baseurl=None, encoding='latin1', debug=False):
        """
        Parameters
        ----------
        baseurl : string or None
            Base URL of the DRMS CGIs. Defaults to JSOC.
        encoding : string
            Character encoding. Defaults to 'latin1'
        debug : boolean
            Enable or disable debug mode. Default is disabled.
        """
        self._json = JsonClient(
            baseurl=baseurl, encoding=encoding, debug=debug)
        self._info_cache = {}

    def __repr__(self):
        return '<Client "%s">' % self.baseurl

    def _convert_numeric_keywords(self, ds, kdf, skip_conversion=None):
        si = self.info(ds)
        int_keys = list(si.keywords[si.keywords.is_integer].index)
        num_keys = list(si.keywords[si.keywords.is_numeric].index)
        num_keys += ['*recnum*', '*sunum*', '*size*']
        if skip_conversion is None:
            skip_conversion = []
        elif isinstance(skip_conversion, six.string_types):
            skip_conversion = [skip_conversion]
        for k in kdf:
            if k in skip_conversion:
                continue
            # pandas apparently does not support hexadecimal strings, so
            # we need a special treatment for integer strings that start
            # with '0x', like QUALITY. The following to_numeric call is
            # still neccessary as the results are still Python objects.
            if k in int_keys and kdf[k].dtype is np.dtype(object):
                idx = kdf[k].str.startswith('0x')
                if idx.any():
                    kdf.loc[idx, k] = kdf.loc[idx, k].map(
                        lambda x: int(x, base=16))
            if k in num_keys:
                kdf[k] = _pd_to_numeric_coerce(kdf.pop(k))

    @property
    def json(self):
        return self._json

    @property
    def baseurl(self):
        return self._json.baseurl

    @baseurl.setter
    def baseurl(self, value):
        self._json.baseurl = value
        self._info_cache = {}

    @property
    def debug(self):
        return self._json.debug

    @debug.setter
    def debug(self, value):
        self._json.debug = value

    def series(self, ds_filter=None):
        """
        List available data series.

        Parameters
        ----------
        ds_filter : string or None
            Regular expression to select a subset of the available series.
            If set to None, a list of all available series is returned.

        Returns
        -------
        result : pandas.DataFrame
            DataFrame containing names, primekeys and notes of the selected
            series.
        """
        d = self._json.show_series(ds_filter)
        if d['status'] != 0:
            raise RuntimeError(
                'DRMS Query failed, status=%d' % d['status'])
        keys = ('name', 'primekeys', 'note')
        if not d['names']:
            return pd.DataFrame(columns=keys)
        recs = [(it['name'], _split_arg(it['primekeys']), it['note'])
                for it in d['names']]
        return pd.DataFrame(recs, columns=keys)

    def info(self, ds):
        """
        Get information about the content of a data series.

        Parameters
        ----------
        ds : string
            Name of the data series.

        Returns
        -------
        result : SeriesInfo
            SeriesInfo instance containing information about the data series.
        """
        m = re.match(r'\s*([\w\.]*)\s*\[*.*\]*', ds)
        name = m.group(1) if m else None
        if name in self._info_cache:
            return self._info_cache[name]
        d = self._json.series_struct(ds)
        if d['status'] != 0:
            raise RuntimeError(
                'DRMS Query failed, status=%d' % d['status'])
        si = SeriesInfo(d, name=name)
        if name is not None:
            self._info_cache[name] = si
        return si

    def keys(self, ds):
        """
        Get a list of keywords that are available for a series. Use the info()
        method for more details.

        Parameters
        ----------
        ds : string
            Name of the data series.

        Returns
        -------
        result : list
            List of keywords available for the selected series.
        """
        si = self.info(ds)
        return list(si.keywords.index)

    def pkeys(self, ds):
        """
        Get a list of primekeys that are available for a series. Use the info()
        method for more details.

        Parameters
        ----------
        ds : string
            Name of the data series.

        Returns
        -------
        result : list
            List of primekeys available for the selected series.
        """
        si = self.info(ds)
        return list(si.primekeys)

    def get(self, ds, key=None, seg=None, link=None, convert_numeric=True,
            skip_conversion=None):
        """
        Query keywords, segments and/or links of a record set. At least one
        of out of the key, seg or link parameters must be specified.

        Parameters
        ----------
        ds : string
            Record set query.
        key : string, list of strings or None
            List of requested keywords, optional.
        seg : string, list of strings or None
            List of requested segments, optional.
        link : string, list of strings or None
            List of requested Links, optional.
        convert_numeric : boolean
            Convert keywords with numeric types from string to numbers. This
            may result in NaNs for invalid/missing values. Default is True.
        skip_conversion : list of strings or None
            List of keywords names to be skipped when performing a numeric
            conversion.

        Returns
        -------
        res_key : pandas.DataFrame (if key is not None)
            Queried keywords
        res_seg : pandas.DataFrame (if seg is not None)
            Queried segments
        res_link : pandas.DataFrame (if link is not None)
            Queried links
        """
        lres = self._json.rs_list(ds, key, seg, link)
        if lres['status'] != 0:
            raise RuntimeError(
                'DRMS Query failed, status=%d' % lres['status'])
        res = []
        if key is not None:
            if 'keywords' in lres:
                names = [it['name'] for it in lres['keywords']]
                values = [it['values'] for it in lres['keywords']]
                res_key = pd.DataFrame(dict(zip(names, values)))
            else:
                res_key = pd.DataFrame()
            if convert_numeric:
                self._convert_numeric_keywords(ds, res_key, skip_conversion)
            res.append(res_key)
        if seg is not None:
            if 'segments' in lres:
                names = [it['name'] for it in lres['segments']]
                values = [it['values'] for it in lres['segments']]
                res_seg = pd.DataFrame(dict(zip(names, values)))
            else:
                res_seg = pd.DataFrame()
            res.append(res_seg)
        if link is not None:
            if 'links' in lres:
                names = [it['name'] for it in lres['links']]
                values = [it['values'] for it in lres['links']]
                res_link = pd.DataFrame(dict(zip(names, values)))
            else:
                res_link = pd.DataFrame()
            res.append(res_link)
        if len(res) == 0:
            return None
        elif len(res) == 1:
            return res[0]
        else:
            return tuple(res)


if __name__ == '__main__':
    def _test_info(c, ds):
        sname = c.series(ds).name
        res = []
        skiplist = [r'jsoc.*']
        for sni in sname:
            skipit = False
            print(sni)
            for spat in skiplist:
                if re.match(spat, sni):
                    print('** skipping series **')
                    skipit = True
                    break
            if not skipit:
                res.append(c.info(sni))
        return res

    c = Client(debug=True)
