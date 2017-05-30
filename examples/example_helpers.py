from __future__ import absolute_import, division, print_function
import os
import os.path as op
import sys
import six


def ask_for_export_email():
    """Ask for a registered email address."""
    print('You have not set the email variable at the top of this script.')
    print('Please set this variable in the script, or enter it below. Note')
    print('that you need to register your email at JSOC first. You can do')
    print('this at: http://jsoc.stanford.edu/ajax/register_email.html')
    try:
        email = six.moves.input('\nPlease enter a REGISTERED email address: ')
    except EOFError:
        email = ''
    print()
    return email


def python_path_prepend(reldir):
    """Prepend relative path to the Python import path list."""
    absdir = op.abspath(op.join(op.dirname(__file__), reldir))
    sys.path.insert(0, absdir)


def is_drms_package_directory(path):
    """Check if the given path is a directory containing the drms package."""
    if not op.isdir(path):
        return False

    init_fpath = op.join(path, '__init__.py')
    if not op.isfile(init_fpath):
        return False

    client_fpath = op.join(path, 'client.py')
    if not op.isfile(client_fpath):
        return False

    try:
        code = open(client_fpath).read()
    except IOError:
        return False

    for s in ['class Client', 'def series', 'def query', 'def export']:
        if s not in code:
            return False

    return True


# If the parent directory contains the drms package, then we assume that we
# are in the drms source directory and add the parent directory to the top
# of the Python import path to make sure that this version of the drms package
# is imported instead of any other installed version.
if is_drms_package_directory(op.join(op.dirname(__file__), '..', 'drms')):
    python_path_prepend('..')
