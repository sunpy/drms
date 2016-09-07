from __future__ import absolute_import, division, print_function
import os
import sys
import six


def python_path_prepend(reldir):
    """Prepend relative path to PYTHON_PATH."""
    absdir = os.path.abspath(os.path.join(os.path.dirname(__file__), reldir))
    sys.path.insert(0, absdir)


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
