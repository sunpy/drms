from urllib.parse import urljoin

__all__ = ['ServerConfig', 'register_server']


class ServerConfig:
    """
    DRMS Server configuration.

    Additional keyword arguments can be used to add additional entries
    to config. In case a keyword argument already exists in the config
    dictionary, the config entry will be replaced by the kwargs value.

    Available config keys are:
        name
        cgi_baseurl
        cgi_show_series
        cgi_jsoc_info
        cgi_jsoc_fetch
        cgi_check_address
        cgi_show_series_wrapper
        show_series_wrapper_dbhost
        url_show_series
        url_jsoc_info
        url_jsoc_fetch
        url_check_address
        url_show_series_wrapper
        encoding
        http_download_baseurl
        ftp_download_baseurl

    Parameters
    ----------
    name : str
        Server configuration name.
    config : dict
        Dictionary containing configuration entries (see below for a
        list of available entries).
    """

    _valid_keys = [
        'name',
        'cgi_baseurl',
        'cgi_show_series',
        'cgi_jsoc_info',
        'cgi_jsoc_fetch',
        'cgi_check_address',
        'cgi_show_series_wrapper',
        'show_series_wrapper_dbhost',
        'url_show_series',
        'url_jsoc_info',
        'url_jsoc_fetch',
        'url_check_address',
        'url_show_series_wrapper',
        'encoding',
        'http_download_baseurl',
        'ftp_download_baseurl',
    ]

    def __init__(self, config=None, **kwargs):
        self._d = d = config.copy() if config is not None else {}
        d.update(kwargs)

        for k in d:
            if k not in self._valid_keys:
                raise ValueError(f'Invalid server config key: {k}')

        if 'name' not in d:
            raise ValueError('Server config entry "name" is missing')

        # encoding defaults to latin1
        if 'encoding' not in d:
            d['encoding'] = 'latin1'

        # Generate URL entries from CGI entries, if cgi_baseurl exists and
        # the specific URL entry is not already set.
        if 'cgi_baseurl' in d:
            cgi_baseurl = d['cgi_baseurl']
            cgi_keys = [k for k in self._valid_keys if k.startswith('cgi') and k != 'cgi_baseurl']
            for k in cgi_keys:
                url_key = f'url{k[3:]}'
                cgi_value = d.get(k)
                if d.get(url_key) is None and cgi_value is not None:
                    d[url_key] = urljoin(cgi_baseurl, cgi_value)

    def __repr__(self):
        return f'<ServerConfig: {self._d.get("name")}>'

    def __dir__(self):
        return dir(type(self)) + list(self.__dict__.keys()) + self._valid_keys

    def __getattr__(self, name):
        if name in self._valid_keys:
            return self._d.get(name)
        else:
            return object.__getattribute__(self, name)

    def __setattr__(self, name, value):
        if name in self._valid_keys:
            if not isinstance(value, str):
                raise ValueError(f'{name} config value must be a string')
            self._d[name] = value
        else:
            object.__setattr__(self, name, value)

    def copy(self):
        return ServerConfig(self._d)

    def to_dict(self):
        return self._d

    def check_supported(self, op):
        """
        Check if an operation is supported by the server.
        """
        if op == 'series':
            return (self.cgi_show_series is not None) or (self.cgi_show_series_wrapper is not None)
        elif op == 'info':
            return self.cgi_jsoc_info is not None
        elif op == 'query':
            return self.cgi_jsoc_info is not None
        elif op == 'email':
            return self.cgi_check_address is not None
        elif op == 'export':
            return (self.cgi_jsoc_info is not None) and (self.cgi_jsoc_fetch is not None)
        else:
            raise ValueError(f'Unknown operation: {op!r}')


def register_server(config):
    """
    Register a server configuration.
    """
    global _server_configs
    name = config.name.lower()
    if name in _server_configs:
        raise RuntimeError(f'ServerConfig {name} already registered')
    _server_configs[config.name.lower()] = config


# Registered servers
_server_configs = {}

# Register public JSOC DRMS server.
register_server(
    ServerConfig(
        name='JSOC',
        cgi_baseurl='http://jsoc.stanford.edu/cgi-bin/ajax/',
        cgi_show_series='show_series',
        cgi_jsoc_info='jsoc_info',
        cgi_jsoc_fetch='jsoc_fetch',
        cgi_check_address='checkAddress.sh',
        cgi_show_series_wrapper='showextseries',
        show_series_wrapper_dbhost='hmidb2',
        http_download_baseurl='http://jsoc.stanford.edu/',
        ftp_download_baseurl='ftp://pail.stanford.edu/export/',
    )
)

# Register KIS DRMS server.
register_server(
    ServerConfig(
        name='KIS',
        cgi_baseurl='http://drms.leibniz-kis.de/cgi-bin/',
        cgi_show_series='show_series',
        cgi_jsoc_info='jsoc_info',
    )
)
