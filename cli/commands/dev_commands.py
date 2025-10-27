import subprocess
import sys
import os
from cli.utils import print_success, print_error, print_info


def format_code_cmd(args):
    """Format code with black"""
    try:
        # Run black on the specified path or current directory
        path = args.path if hasattr(args, "path") and args.path else "."
        result = subprocess.run(
            [sys.executable, "-m", "black", path],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )
        if result.returncode == 0:
            if result.stdout.strip():
                print(result.stdout)
            print_success("Code formatted successfully")
        else:
            print_error("Black formatting failed")
            if result.stderr:
                print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print_error("Black is not installed. Run: pip install black")
        return 1
    except Exception as e:
        print_error(f"Error running black: {e}")
        return 1


def lint_code_cmd(args):
    """Lint code with flake8"""
    try:
        # Run flake8 on the specified path or current directory
        path = args.path if hasattr(args, "path") and args.path else "."
        result = subprocess.run(
            [sys.executable, "-m", "flake8", path],
            capture_output=True,
            text=True,
            cwd=os.getcwd(),
        )
        if result.returncode == 0:
            print_success("No linting issues found")
        else:
            print("Linting issues found:")
            if result.stdout:
                print(result.stdout)
            if result.stderr:
                print(result.stderr)
        return result.returncode
    except FileNotFoundError:
        print_error("Flake8 is not installed. Run: pip install flake8")
        return 1
    except Exception as e:
        print_error(f"Error running flake8: {e}")
        return 1
