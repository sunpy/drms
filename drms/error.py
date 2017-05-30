from __future__ import absolute_import, division, print_function

__all__ = ['DrmsError', 'DrmsQueryError', 'DrmsExportError',
           'DrmsOperationNotSupported']


class DrmsError(RuntimeError):
    """
    Unspecified DRMS run-time error.
    """
    pass


class DrmsQueryError(DrmsError):
    """
    DRMS query error.
    """
    pass


class DrmsExportError(DrmsError):
    """
    DRMS data export error.
    """
    pass


class DrmsOperationNotSupported(DrmsError):
    """
    Operation is not supported by DRMS server.
    """
    pass
