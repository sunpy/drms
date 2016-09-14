from __future__ import absolute_import, division, print_function

__all__ = ['DrmsError', 'DrmsQueryError', 'DrmsExportError']


class DrmsError(RuntimeError):
    pass


class DrmsQueryError(DrmsError):
    pass


class DrmsExportError(DrmsError):
    pass
