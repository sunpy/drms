import json as _json
from urllib.parse import urlencode, quote_plus
from urllib.request import urlopen

from .config import ServerConfig, _server_configs
from .utils import _split_arg

__all__ = ['const', 'HttpJsonRequest', 'HttpJsonClient']


class JsocInfoConstants:
    """
    Constants for DRMS queries.

    Attributes
    ----------
    all
        = ``'**ALL**'``
    none
        = ``'**NONE**'``
    recdir
        = ``'*recdir*'``
    dirmtime
        = ``'*dirmtime*'``
    logdir
        = ``'*logdir*'``
    recnum
        = ``'*recnum*'``
    sunum
        = ``'*sunum*'``
    size
        = ``'*size*'``
    online
        = ``'*online*'``
    retain
        = ``'*retain*'``
    archive
        = ``'*archive*'``
    """

    all = '**ALL**'
    none = '**NONE**'
    recdir = '*recdir*'
    dirmtime = '*dirmtime*'
    logdir = '*logdir*'
    recnum = '*recnum*'
    sunum = '*sunum*'
    size = '*size*'
    online = '*online*'
    retain = '*retain*'
    archive = '*archive*'


const = JsocInfoConstants()


class HttpJsonRequest:
    """
    Class for handling HTTP/JSON requests.

    Use `HttpJsonClient` to create an instance.
    """

    def __init__(self, url, encoding):
        self._encoding = encoding
        self._http = urlopen(url)
        self._data_str = None
        self._data = None

    def __repr__(self):
        return f'<HttpJsonRequest: {self.url}>'

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
            self._data = _json.loads(self.raw_data.decode(self._encoding))
        return self._data


class HttpJsonClient:
    """
    HTTP/JSON communication with the DRMS server CGIs.

    Parameters
    ----------
    server : str or drms.config.ServerConfig
        Registered server ID or ServerConfig instance.
        Defaults to JSOC.
    debug : bool
        Enable or disable debug mode (default is disabled).
    """

    def __init__(self, server='jsoc', debug=False):
        if isinstance(server, ServerConfig):
            self._server = server
        else:
            self._server = _server_configs[server.lower()]
        self.debug = debug

    def __repr__(self):
        return f'<HttpJsonClient: {self._server.name}>'

    def _json_request(self, url):
        if self.debug:
            print(url)
        return HttpJsonRequest(url, self._server.encoding)

    @property
    def server(self):
        return self._server

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
        ds_filter : str
            Name filter regexp.

        Returns
        -------
        result : dict
        """
        query = '?' if ds_filter is not None else ""
        if ds_filter is not None:
            query += urlencode({'filter': ds_filter})
        req = self._json_request(self._server.url_show_series + query)
        return req.data

    def show_series_wrapper(self, ds_filter=None, info=False):
        """
        List available data series.

        This is an alternative to show_series, which needs to be used
        to get a list of all available series provided by JSOC. There
        is currently no support for retrieving primekeys using this
        CGI.

        Parameters
        ----------
        ds_filter : str
            Name filter regexp.
        info : bool
            If False (default), the result only contains series names.
            If set to True, the result includes a description for each
            series.

        Returns
        -------
        result : dict
        """
        query_args = {'dbhost': self._server.show_series_wrapper_dbhost}
        if ds_filter is not None:
            query_args['filter'] = ds_filter
        if info:
            query_args['info'] = '1'
        query = f'?{urlencode(query_args)}'
        req = self._json_request(self._server.url_show_series_wrapper + query)
        return req.data

    def series_struct(self, ds):
        """
        Get information about the content of a data series.

        Parameters
        ----------
        ds : str
            Name of the data series.

        Returns
        -------
        result : dict
            Dictionary containing information about the data series.
        """
        query = f'?{urlencode({"op": "series_struct", "ds": ds})}'
        req = self._json_request(self._server.url_jsoc_info + query)
        return req.data

    def rs_summary(self, ds):
        """
        Get summary (i.e. count) of a given record set.

        Parameters
        ----------
        ds : str
            Record set query (only one series).

        Returns
        -------
        result : dict
            Dictionary containg 'count', 'status' and 'runtime'.
        """
        query = f'?{urlencode({"op": "rs_summary", "ds": ds})}'
        req = self._json_request(self._server.url_jsoc_info + query)
        return req.data

    def rs_list(self, ds, key=None, seg=None, link=None, recinfo=False, n=None, uid=None):
        """
        Get detailed information about a record set.

        Parameters
        ----------
        ds : str
            Record set query.
        key : str, list or None
            List of requested keywords, optional.
        seg : str, list or None
            List of requested segments, optional.
        link : str or None
            List of requested Links, optional.
        recinfo : bool
            Request record info for each record in the record set.
        n : int or None
            Record set limit. For positive values, the first n records
            of the record set are returned, for negative values the
            last abs(n) records. If set to None (default), no limit is
            applied.
        uid : str or None
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
        if recinfo:
            d['R'] = '1'
        if n is not None:
            d['n'] = f'{int(int(n))}'
        if uid is not None:
            d['userhandle'] = uid
        query = f'?{urlencode(d)}'
        req = self._json_request(self._server.url_jsoc_info + query)
        return req.data

    def check_address(self, email):
        """
        Check if an email address is registered for export data requests.

        Parameters
        ----------
        email : str
            Email address to be verified.

        Returns
        -------
        result : dict
            Dictionary containing 'status' and 'msg'.

            Some status codes are:
            - 2: Email address is valid and registered
            - 4: Email address has neither been validated nor registered
            - -2: Not a valid email address
        """
        query = '?' + urlencode({'address': quote_plus(email), 'checkonly': '1'})
        req = self._json_request(self._server.url_check_address + query)
        return req.data

    def exp_request(self, *args, **kwargs):
        """
        Request data export.

        Parameters
        ----------
        ds : str
            Data export record set query.
        notify : str
            Registered email address.
        method : str
            Export method. Supported methods are: 'url_quick', 'url',
            'url-tar', 'ftp' and 'ftp-tar'. Default is 'url_quick'.
        protocol : str
            Export protocol. Supported protocols are: 'as-is', 'fits',
            'jpg', 'mpg' and 'mp4'. Default is 'as-is'.
        protocol_args : dict or None
            Extra protocol arguments for protocols 'jpg', 'mpg' and
            'mp4'. Valid arguments are: 'ct', 'scaling', 'min', 'max'
            and 'size'.
        filenamefmt : str, None
            Custom filename format string for exported files. This is
            ignored for 'url_quick'/'as-is' data exports.
        process : `dict`, None
            Dictionary of processing commands. Each entry is also a `dict`
            containing all of the applicable options for that processing
            command.
        n : int or None
            Limits the number of records requested. For positive
            values, the first n records of the record set are returned,
            for negative values the last abs(n) records. If set to None
            (default), no limit is applied.
        requestor : str, None or bool
            Export user ID. Default is None, in which case the user
            name is determined from the email address. If set to False,
            the requestor argument will be omitted in the export
            request.

        Returns
        -------
        result : dict
            Dictionary containing the server response to the export
            request.
        """
        req = self._json_request(self._exp_request_url(*args, **kwargs))
        return req.data

    def _exp_request_url(
        self,
        ds,
        notify,
        method='url_quick',
        protocol='as-is',
        protocol_args=None,
        filenamefmt=None,
        n=None,
        process=None,
        requestor=None,
    ):
        method = method.lower()
        method_list = ['url_quick', 'url', 'url-tar', 'ftp', 'ftp-tar']
        if method not in method_list:
            raise ValueError(
                'Method {} is not supported, valid methods are: {}'.format(
                    method, ', '.join(str(s) for s in method_list)
                )
            )

        protocol = protocol.lower()
        img_protocol_list = ['jpg', 'mpg', 'mp4']
        protocol_list = ['as-is', 'fits'] + img_protocol_list
        if protocol not in protocol_list:
            raise ValueError(
                'Protocol {} is not supported, valid protocols are: {}'.format(
                    protocol, ', '.join(str(s) for s in protocol_list)
                )
            )

        # method "url_quick" is meant to be used with "as-is", change method
        # to "url" if protocol is not "as-is"
        if method == 'url_quick' and protocol != 'as-is':
            method = 'url'

        if protocol in img_protocol_list:
            extra_keys = {'ct': 'grey.sao', 'scaling': 'MINMAX', 'size': 1}
            if protocol_args is not None:
                for k, v in protocol_args.items():
                    if k.lower() == 'ct':
                        extra_keys['ct'] = v
                    elif k == 'scaling':
                        extra_keys[k] = v
                    elif k == 'size':
                        extra_keys[k] = int(v)
                    elif k in ['min', 'max']:
                        extra_keys[k] = float(v)
                    else:
                        raise ValueError(f'Unknown protocol argument: {k}')
            protocol += ',CT={ct},scaling={scaling},size={size}'.format(**extra_keys)
            if 'min' in extra_keys:
                protocol += f',min={extra_keys["min"]:g}'
            if 'max' in extra_keys:
                protocol += f',max={extra_keys["max"]:g}'
        else:
            if protocol_args is not None:
                raise ValueError(f'protocol_args not supported for protocol {protocol}')

        d = {
            'op': 'exp_request',
            'format': 'json',
            'ds': ds,
            'notify': notify,
            'method': method,
            'protocol': protocol,
        }

        if filenamefmt is not None:
            d['filenamefmt'] = filenamefmt

        n = int(n) if n is not None else 0
        d['process=n'] = f'{n}'
        if process is not None:
            allowed_processes = [
                'im_patch',
                'resize',
                'rebin',
                'aia_scale_aialev1',
                'aia_scale_orig',
                'aia_scale_other',
                'Maproj',
                'HmiB2ptr',
            ]
            process_strings = {}
            for p, opts in process.items():
                if p not in allowed_processes:
                    raise ValueError(f'{p} is not one of the allowed processing options: {allowed_processes}')
                process_strings[p] = ','.join([f'{k}={v}' for k, v in opts.items()])
            processes = '|'.join([f'{k},{v}' for k, v in process_strings.items()])
            d['process=n'] = f'{d["process=n"]}|{processes}'

        if requestor is None:
            d['requestor'] = notify.split('@')[0]
        elif requestor is not False:
            d['requestor'] = requestor

        query = '?' + urlencode(d)
        return self._server.url_jsoc_fetch + query

    def exp_status(self, requestid):
        """
        Query data export status.

        Parameters
        ----------
        requestid : str
            Request identifier returned by exp_request.

        Returns
        -------
        result : dict
            Dictionary containing the export request status.
        """
        query = f'?{urlencode({"op": "exp_status", "requestid": requestid})}'
        req = self._json_request(self._server.url_jsoc_fetch + query)
        return req.data
