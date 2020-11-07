import pytest

from drms.config import ServerConfig, _server_configs, register_server


def test_create_config_basic():
    cfg = ServerConfig(name='TEST')
    valid_keys = ServerConfig._valid_keys
    assert 'name' in valid_keys
    assert 'encoding' in valid_keys
    for k in valid_keys:
        v = getattr(cfg, k)
        if k == 'name':
            assert v == 'TEST'
        elif k == 'encoding':
            assert v == 'latin1'
        else:
            assert v is None
    assert repr(cfg) == '<ServerConfig: TEST>'


def test_create_config_missing_name():
    with pytest.raises(ValueError):
        ServerConfig()


def test_copy_config():
    cfg = ServerConfig(name='TEST')
    assert cfg.name == 'TEST'

    cfg2 = cfg.copy()
    assert cfg2 is not cfg
    assert cfg2.name == 'TEST'

    cfg.name = 'MUH'
    assert cfg.name != cfg2.name


def test_register_server():
    cfg = ServerConfig(name='TEST')

    assert 'test' not in _server_configs
    register_server(cfg)
    assert 'test' in _server_configs

    del _server_configs['test']
    assert 'test' not in _server_configs


def test_register_server_existing():
    assert 'jsoc' in _server_configs
    cfg = ServerConfig(name='jsoc')
    with pytest.raises(RuntimeError):
        register_server(cfg)
    assert 'jsoc' in _server_configs


def test_config_jsoc():
    assert 'jsoc' in _server_configs

    cfg = _server_configs['jsoc']
    assert cfg.name.lower() == 'jsoc'
    assert isinstance(cfg.encoding, str)
    assert isinstance(cfg.cgi_show_series, str)
    assert isinstance(cfg.cgi_jsoc_info, str)
    assert isinstance(cfg.cgi_jsoc_fetch, str)
    assert isinstance(cfg.cgi_check_address, str)
    assert isinstance(cfg.cgi_show_series_wrapper, str)
    assert isinstance(cfg.show_series_wrapper_dbhost, str)
    assert cfg.http_download_baseurl.startswith('http://')
    assert cfg.ftp_download_baseurl.startswith('ftp://')

    baseurl = cfg.cgi_baseurl
    assert baseurl.startswith('http://')
    assert cfg.url_show_series.startswith(baseurl)
    assert cfg.url_jsoc_info.startswith(baseurl)
    assert cfg.url_jsoc_fetch.startswith(baseurl)
    assert cfg.url_check_address.startswith(baseurl)
    assert cfg.url_show_series_wrapper.startswith(baseurl)


def test_config_kis():
    assert 'kis' in _server_configs
    cfg = _server_configs['kis']

    assert cfg.name.lower() == 'kis'
    assert isinstance(cfg.encoding, str)

    assert isinstance(cfg.cgi_show_series, str)
    assert isinstance(cfg.cgi_jsoc_info, str)
    assert cfg.cgi_jsoc_fetch is None
    assert cfg.cgi_check_address is None
    assert cfg.cgi_show_series_wrapper is None
    assert cfg.show_series_wrapper_dbhost is None
    assert cfg.http_download_baseurl is None
    assert cfg.ftp_download_baseurl is None

    baseurl = cfg.cgi_baseurl
    assert baseurl.startswith('http://')
    assert cfg.url_show_series.startswith(baseurl)
    assert cfg.url_jsoc_info.startswith(baseurl)
    assert cfg.url_jsoc_fetch is None
    assert cfg.url_check_address is None
    assert cfg.url_show_series_wrapper is None


@pytest.mark.parametrize(
    'server_name, operation, expected',
    [
        ('jsoc', 'series', True),
        ('jsoc', 'info', True),
        ('jsoc', 'query', True),
        ('jsoc', 'email', True),
        ('jsoc', 'export', True),
        ('kis', 'series', True),
        ('kis', 'info', True),
        ('kis', 'query', True),
        ('kis', 'email', False),
        ('kis', 'export', False),
    ],
)
def test_supported(server_name, operation, expected):
    cfg = _server_configs[server_name]
    assert cfg.check_supported(operation) == expected


@pytest.mark.parametrize(
    'server_name, operation', [('jsoc', 'bar'), ('kis', 'foo')],
)
def test_supported_invalid_operation(server_name, operation):
    cfg = _server_configs[server_name]
    with pytest.raises(ValueError):
        cfg.check_supported(operation)


def test_create_config_invalid_key():
    with pytest.raises(ValueError):
        cfg = ServerConfig(foo='bar')


def test_getset_attr():
    cfg = ServerConfig(name='TEST')
    assert getattr(cfg, 'name') == 'TEST'
    assert getattr(cfg, '__dict__') == {'_d': {'encoding': 'latin1', 'name': 'TEST'}}
    with pytest.raises(AttributeError):
        getattr(cfg, 'foo')
    setattr(cfg, 'name', 'NewTest')
    assert getattr(cfg, 'name') == 'NewTest'
    with pytest.raises(ValueError):
        setattr(cfg, 'name', 123)
    setattr(cfg, '__sizeof__', 127)
    assert getattr(cfg, '__sizeof__') == 127


def test_to_dict():
    cfg = ServerConfig(name='TEST')
    _dict = cfg.to_dict()
    assert isinstance(_dict, dict)
    assert _dict == {'encoding': 'latin1', 'name': 'TEST'}


def test_inbuilt_dir():
    cfg = ServerConfig(name='TEST')
    valid_keys = ServerConfig._valid_keys
    list_attr = dir(cfg)
    assert isinstance(list_attr, list)
    assert set(dir(object)).issubset(set(list_attr))
    assert set(valid_keys).issubset(set(list_attr))
    assert set(list(cfg.__dict__.keys())).issubset(set(list_attr))
