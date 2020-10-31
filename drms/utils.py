import os
import re
from functools import partial

import numpy as np
import pandas as pd
import pkg_resources

__all__ = ['to_datetime']


def _pd_to_datetime_coerce(arg):
    return pd.to_datetime(arg, errors='coerce')


def _pd_to_numeric_coerce(arg):
    return pd.to_numeric(arg, errors='coerce')


def _split_arg(arg):
    """
    Split a comma-separated string into a list.
    """
    if isinstance(arg, str):
        arg = [it for it in re.split(r'[\s,]+', arg) if it]
    return arg


def _extract_series_name(ds):
    """
    Extract series name from record set.
    """
    m = re.match(r'^\s*([\w\.]+).*$', ds)
    return m.group(1) if m is not None else None


def to_datetime(tstr, force=False):
    """
    Parse JSOC time strings.

    In general, this is quite complicated, because of the many
    different (non-standard) time strings supported by the DRMS. For
    more (much more!) details on this matter, see
    `Rick Bogart's notes <http://jsoc.stanford.edu/doc/timerep.html>`__.

    The current implementation only tries to convert typical HMI time
    strings, with a format like "%Y.%m.%d_%H:%M:%S_TAI", to an ISO time
    string, that is then parsed by pandas. Note that "_TAI", aswell as
    other timezone indentifiers like "Z", will not be taken into
    account, so the result will be a naive timestamp without any
    associated timezone.

    If you know the time string format, it might be better calling
    pandas.to_datetime() directly. For handling TAI timestamps, e.g.
    converting between TAI and UTC, the astropy.time package can be
    used.

    Parameters
    ----------
    tstr : string or list/Series of strings
        DateTime strings.
    force : bool
        Set to True to omit the endswith('_TAI') check.

    Returns
    -------
    result : pandas.Series or pandas.Timestamp
        Pandas series or a single Timestamp object.
    """
    s = pd.Series(tstr).astype(str)
    if force or s.str.endswith('_TAI').any():
        s = s.str.replace('_TAI', "")
        s = s.str.replace('_', ' ')
        s = s.str.replace('.', '-', n=2)
    res = _pd_to_datetime_coerce(s)
    res = res.dt.tz_localize(None)
    return res.iloc[0] if (len(res) == 1) and np.isscalar(tstr) else res


def generate_changelog_for_docs(directory, output_filename=None):
    """
    This is a modified version of the `towncrier._main` function with a few
    things disabled.

    This function is based heavily on towncrier, please see
    licenses/TOWNCRIER.rst
    """
    from towncrier import (
        _get_date,
        append_to_newsfile,
        find_fragments,
        get_project_name,
        get_version,
        load_config,
        render_fragments,
        split_fragments,
    )

    print('Updating Changelog...')
    directory = os.path.abspath(directory)
    _join_dir = partial(os.path.join, directory)
    config = load_config(directory)
    if not config:
        raise FileNotFoundError(f'Could not locate the towncrier config file at path {directory}.')

    print('Loading template...')
    if config['template'] is None:
        template = pkg_resources.resource_string('towncrier', 'templates/template.rst').decode('utf8')
    else:
        with open(config['template'], 'rb') as tmpl:
            template = tmpl.read().decode('utf8')

    print('Finding news fragments...')

    definitions = config['types']

    if config.get('directory'):
        base_directory = _join_dir(config['directory'])
        fragment_directory = None

    fragments, fragment_filenames = find_fragments(
        base_directory, config['sections'], fragment_directory, definitions
    )

    print('Rendering news fragments...')
    fragments = split_fragments(fragments, definitions)
    rendered = render_fragments(
        # The 0th underline is used for the top line
        template,
        config['issue_format'],
        fragments,
        definitions,
        config['underlines'][1:],
        config['wrap'],
    )

    project_version = get_version(_join_dir(config['package_dir']), config['package'])

    package = config.get('package')
    if package:
        project_name = get_project_name(os.path.abspath(_join_dir(config['package_dir'])), package)
    else:
        # Can't determine a project_name, but maybe it is not needed.
        project_name = ""

    project_date = _get_date()

    top_line = config['title_format'].format(name=project_name, version=project_version, project_date=project_date)
    top_line += f'\n{config["underlines"][0] * len(top_line)}\n'

    print('Writing to newsfile...')
    start_line = config['start_line']
    if not output_filename:
        output_filename = _join_dir(config['filename'])
    output_filename = os.path.abspath(output_filename)
    append_to_newsfile(directory, output_filename, start_line, top_line, rendered)

    print('Done!')
