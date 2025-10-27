#!/usr/bin/env python3
"""
FAF Explorer - Main entry point
"""
import sys
import argparse
import subprocess
import os
from cli import main


def run_interactive():
    print("FAF Explorer Interactive Mode")
    print("Type 'exit' to quit")
    while True:
        try:
            command = input("faf> ").strip()
            if command.lower() == "exit":
                break
            if command:
                # Split command into args
                args = command.split()
                # Temporarily set sys.argv
                original_argv = sys.argv
                sys.argv = ["faf.py"] + args
                try:
                    main()
                except SystemExit:
                    pass  # argparse exits with SystemExit
                finally:
                    sys.argv = original_argv
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            break


def run_pytest():
    """Run pytest on the project"""
    try:
        # Run pytest in the current directory
        result = subprocess.run(
            [sys.executable, "-m", "pytest"],
            cwd=os.getcwd(),
            capture_output=True,
            text=True,
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr, file=sys.stderr)
        return result.returncode
    except Exception as e:
        print(f"Error running pytest: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="FAF Explorer")
    parser.add_argument("--run", action="store_true", help="Run in interactive mode")
    parser.add_argument("--cli", action="store_true", help="CLI mode (used with --run)")
    parser.add_argument(
        "--pytest", action="store_true", help="Run pytest on the project"
    )

    args, remaining = parser.parse_known_args()

    if args.pytest:
        sys.exit(run_pytest())
    elif args.run and args.cli:
        run_interactive()
    else:
        # Normal mode, pass remaining args to main
        sys.argv = ["faf.py"] + remaining
        sys.exit(main())
