#!/usr/bin/env python3
"""
FAF Explorer - Main CLI Entry Point
"""

import sys
import os
import argparse
import subprocess
import json

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load project configuration
def load_project_config():
    """Load project configuration from config/project.json"""
    config_path = os.path.join(os.path.dirname(__file__), 'config', 'project.json')
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Fallback configuration
        return {
            "name": "FAF Explorer",
            "version": "1.0.0",
            "description": "A powerful dual-interface file and folder management tool with CLI and GUI"
        }

# Load configuration
config = load_project_config()

# Display version and description
print(f"{config['name']} v{config['version']}")
print(config['description'])
print()

# Import and run CLI
from cli.main import main

# Import project manager for additional functionality
from faf_explorer.project_manager import ProjectManager


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


def run_gui():
    """Run the GUI application"""
    try:
        from ui.main import main as gui_main
        gui_main()
    except Exception as e:
        print(f"Error running GUI: {e}", file=sys.stderr)
        return 1


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
    parser = argparse.ArgumentParser(description=config['description'])
    parser.add_argument("--run", action="store_true", help="Run in interactive mode")
    parser.add_argument("--cli", action="store_true", help="CLI mode (used with --run)")
    parser.add_argument("--gui", action="store_true", help="Run GUI mode")
    parser.add_argument(
        "--pytest", action="store_true", help="Run pytest on the project"
    )

    args, remaining = parser.parse_known_args()

    if args.pytest:
        sys.exit(run_pytest())
    elif args.run and args.cli:
        run_interactive()
    elif args.run and args.gui:
        run_gui()
    else:
        # Normal mode, pass remaining args to main
        sys.argv = ["faf.py"] + remaining
        sys.exit(main())
