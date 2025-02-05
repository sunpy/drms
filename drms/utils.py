import re
import sys
from urllib.request import Request

import numpy as np
import pandas as pd
from packaging.version import Version

import drms

__all__ = ["create_request_with_header", "to_datetime"]

PD_VERSION = Version(pd.__version__)


def create_request_with_header(url):
    request = Request(url)
    request.add_header("User-Agent", f"drms/{drms.__version__}, python/{sys.version[:5]}")
    return request


def _pd_to_datetime_coerce(arg):
    if PD_VERSION >= Version("2.0.0"):
        return pd.to_datetime(arg, errors="coerce", format="mixed", dayfirst=False)
    return pd.to_datetime(arg, errors="coerce")


def _pd_to_numeric_coerce(arg):
    return pd.to_numeric(arg, errors="coerce")


def _split_arg(arg):
    """
    Split a comma-separated string into a list.
    """
    if isinstance(arg, str):
        return [it for it in re.split(r"[\s,]+", arg) if it]
    return arg


def _extract_series_name(ds):
    """
    Extract series name from record set.
    """
    m = re.match(r"^\s*([\w\.]+).*$", ds)
    return m.group(1) if m is not None else None


def to_datetime(tstr, *, force=False):
    """
    Parse JSOC time strings.

    In general, this is quite complicated, because of the many
    different (non-standard) time strings supported by the DRMS. For
    more (much more!) details on this matter, see
    `Rick Bogart's notes <http://jsoc.stanford.edu/doc/timerep.html>`__.

    The current implementation only tries to convert typical HMI time
    strings, with a format like "%Y.%m.%d_%H:%M:%S_TAI", to an ISO time
    string, that is then parsed by pandas. Note that "_TAI", as well as
    other timezone identifiers like "Z", will not be taken into
    account, so the result will be a naive timestamp without any
    associated timezone.

    If you know the time string format, it might be better calling
    pandas.to_datetime() directly. For handling TAI timestamps, e.g.
    converting between TAI and UTC, the astropy.time package can be
    used.

    Parameters
    ----------
    tstr : str or List[str] or pandas.Series
        Datetime strings.
    force : bool
        Set to True to omit the ``endswith('_TAI')`` check.

    Returns
    -------
    result : pandas.Series or pandas.Timestamp
        Pandas series or a single Timestamp object.
    """
    date = pd.Series(tstr, dtype=object).astype(str)
    if force or date.str.endswith("_TAI").any():
        date = date.str.replace("_TAI", "")
        date = date.str.replace("_", " ")
        if PD_VERSION >= Version("2.0.0"):
            regex = False
        else:
            regex = True
        date = date.str.replace(".", "-", regex=regex, n=2)
    res = _pd_to_datetime_coerce(date)
    res = res.dt.tz_localize(None)
    return res.iloc[0] if (len(res) == 1) and np.isscalar(tstr) else res
