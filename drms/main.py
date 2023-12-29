import sys
import argparse


def main():
    import drms

    args = parse_args(sys.argv[1:])
    client = drms.Client(server=args.server, email=args.email)
    drms.logger.info(f"client: {client}")


def parse_args(args):
    import drms

    parser = argparse.ArgumentParser(description="drms, access HMI, AIA and MDI data with python")
    parser.add_argument(
        "--version",
        action="version",
        version=f"drms v{drms.__version__}",
        help="show package version and exit",
    )
    parser.add_argument("--email", help="email address for data export requests")
    parser.add_argument("server", nargs="?", default="jsoc", help="DRMS server, default is JSOC")

    return parser.parse_args(args)
