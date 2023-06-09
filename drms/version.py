# NOTE: First try _dev.scm_version if it exists and setuptools_scm is installed
# This file is not included in muse wheels/tarballs, so otherwise it will
# fall back on the generated _version module.
try:
    try:
        from ._dev.scm_version import version
    except ImportError:
        from ._version import version
except Exception:  # NOQA: BLE001
    import warnings

    warnings.warn(
        f'could not determine {__name__.split(".")[0]} package version; this indicates a broken installation',
        stacklevel=3,
    )
    del warnings
    version = "0.0.0"

from packaging.version import parse as _parse

_version = _parse(version)
major, minor, bugfix = [*_version.release, 0][:3]
release = not _version.is_devrelease
