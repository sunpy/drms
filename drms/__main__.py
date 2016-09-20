from __future__ import absolute_import, division, print_function
import argparse as _argparse
import drms

# Handle command line options
_arg_parser = _argparse.ArgumentParser('drms')
_arg_parser.add_argument(
    '--debug', action='store_true', help='enable debug output')
_arg_parser.add_argument(
    '--version', action='version', version='drms %s' % drms.__version__,
    help='show package version and exit')
_arg_parser.add_argument(
    '--email', help='email address for data export requests')
_arg_parser.add_argument(
    '--verbose', action='store_true',
    help='print export status messages to stdout')
_arg_parser.add_argument(
    'server', nargs='?', default='jsoc', help='DRMS server, default is JSOC')
_args = _arg_parser.parse_args()

# Create a Client instance
c = drms.Client(_args.server, email=_args.email, verbose=_args.verbose,
                debug=_args.debug)
print('c = %r' % c)
