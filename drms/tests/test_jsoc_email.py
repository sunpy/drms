import pytest

import drms
from drms.config import ServerConfig
from drms.exceptions import DrmsOperationNotSupported

# Invalid email addresses used for testing
invalid_emails = [
    "notregistered@example.com",
    "not-valid",
    "",
]


@pytest.mark.jsoc()
@pytest.mark.remote_data()
@pytest.mark.parametrize("email", invalid_emails)
def test_email_invalid_check(email):
    c = drms.Client("jsoc")
    assert not c.check_email(email)


@pytest.mark.jsoc()
@pytest.mark.remote_data()
@pytest.mark.parametrize("email", invalid_emails)
def test_email_invalid_set(email):
    c = drms.Client("jsoc")
    with pytest.raises(ValueError, match="Email address is invalid or not registered"):
        c.email = email


@pytest.mark.jsoc()
@pytest.mark.remote_data()
@pytest.mark.parametrize("email", invalid_emails)
def test_email_invalid_init(email):
    with pytest.raises(ValueError, match="Email address is invalid or not registered"):
        drms.Client("jsoc", email=email)


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_email_cmdopt_check(email):
    c = drms.Client("jsoc")
    assert c.check_email(email)


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_email_cmdopt_set(email):
    c = drms.Client("jsoc")
    c.email = email
    assert c.email == email


@pytest.mark.jsoc()
@pytest.mark.remote_data()
def test_email_cmdopt_init(email):
    c = drms.Client("jsoc", email=email)
    assert c.email == email


def test_query_invalid():
    cfg = ServerConfig(name="TEST")
    with pytest.raises(DrmsOperationNotSupported):
        drms.Client(cfg, email="user@example.com")
