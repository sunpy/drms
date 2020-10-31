import sys
import argparse


def main():
    import drms

    args = parse_args(sys.argv[1:])

    # Create a Client instance
    client = drms.Client(args.server, email=args.email, verbose=args.verbose, debug=args.debug)
    print(f'client: {client}')


def parse_args(args):
    import drms

    # Handle command line options
    parser = argparse.ArgumentParser(description='drms, access HMI, AIA and MDI data with python')
    parser.add_argument('--debug', action='store_true', help='enable debug output')
    parser.add_argument(
        '--version', action='version', version=f'drms v{drms.__version__}', help='show package version and exit',
    )
    parser.add_argument('--email', help='email address for data export requests')
    parser.add_argument('--verbose', action='store_true', help='print export status messages to stdout')
    parser.add_argument('server', nargs='?', default='jsoc', help='DRMS server, default is JSOC')

    args = parser.parse_args(args)
    return args
