from __future__ import absolute_import, division, print_function

__all__ = ['DrmsError', 'DrmsQueryError', 'DrmsExportError']


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
