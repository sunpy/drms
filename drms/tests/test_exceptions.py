import pytest

import drms


@pytest.mark.parametrize(
    'exception_class', [drms.DrmsError, drms.DrmsQueryError, drms.DrmsExportError, drms.DrmsOperationNotSupported],
)
def test_exception_class(exception_class):
    with pytest.raises(RuntimeError):
        raise exception_class()
    with pytest.raises(drms.DrmsError):
        raise exception_class()
