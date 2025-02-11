__all__ = [
    "DrmsError",
    "DrmsExportError",
    "DrmsOperationNotSupported",
    "DrmsQueryError",
]


class DrmsError(RuntimeError):
    """
    Unspecified DRMS run-time error.
    """


class DrmsQueryError(DrmsError):
    """
    DRMS query error.
    """


class DrmsExportError(DrmsError):
    """
    DRMS data export error.
    """


class DrmsOperationNotSupported(DrmsError):
    """
    Operation is not supported by DRMS server.
    """
