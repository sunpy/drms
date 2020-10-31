import pytest

import drms

# Invalid email addresses used for testing
invalid_emails = [
    'notregistered@example.com',
    'not-valid',
    "",
]


@pytest.mark.jsoc
@pytest.mark.remote_data
@pytest.mark.parametrize('email', invalid_emails)
def test_email_invalid_check(email):
    c = drms.Client('jsoc')
    assert not c.check_email(email)


@pytest.mark.jsoc
@pytest.mark.remote_data
@pytest.mark.parametrize('email', invalid_emails)
def test_email_invalid_set(email):
    c = drms.Client('jsoc')
    with pytest.raises(ValueError):
        c.email = email


@pytest.mark.jsoc
@pytest.mark.remote_data
@pytest.mark.parametrize('email', invalid_emails)
def test_email_invalid_init(email):
    with pytest.raises(ValueError):
        drms.Client('jsoc', email=email)


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_email_cmdopt_check(email):
    c = drms.Client('jsoc')
    assert c.check_email(email)


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_email_cmdopt_set(email):
    c = drms.Client('jsoc')
    c.email = email
    assert c.email == email


@pytest.mark.jsoc
@pytest.mark.export
@pytest.mark.remote_data
def test_email_cmdopt_init(email):
    c = drms.Client('jsoc', email=email)
    assert c.email == email
