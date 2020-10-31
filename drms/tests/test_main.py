import sys

import pytest

from drms.main import main, parse_args


def helper(args, name, expected):
    args = parse_args(args)
    assert getattr(args, name) == expected


def test_debug():
    helper(['--debug'], 'debug', True)
    helper([], 'debug', False)


def test_verbose():
    helper(['--verbose'], 'verbose', True)
    helper([], 'verbose', False)


def test_version():
    with pytest.raises(SystemExit):
        helper(['--version'], 'version', True)


def test_server():
    helper(['fake_url_server'], 'server', 'fake_url_server')
    helper([], 'server', 'jsoc')


def test_email():
    helper(['--email', 'fake@gmail.com'], 'email', 'fake@gmail.com')
    helper([], 'email', None)


def test_main_empty():
    sys.argv = [
        'drms',
    ]
    main()
