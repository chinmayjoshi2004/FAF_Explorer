#!/usr/bin/env python3
"""
FAF Explorer CLI - File and Folder Explorer Command Line Interface
"""

from cli.parsers import setup_parsers
from cli.utils import print_error


def main():
    parser = setup_parsers()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if hasattr(args, "func"):
        args.func(args)
    else:
        print_error("Invalid command. Use --help for usage information.")


if __name__ == "__main__":
    main()
