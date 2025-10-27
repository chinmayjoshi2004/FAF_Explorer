"""
FAF Explorer Project Manager - Handles installation, updates, and project management
"""

import os
import sys
import json
import subprocess
import urllib.request
import zipfile
import shutil
from pathlib import Path
import platform


class ProjectManager:
    """Project manager for FAF Explorer installation and updates"""

    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.config_path = self.project_root / 'config' / 'project.json'
        self.config = self.load_config()

    def load_config(self):
        """Load project configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading config: {e}")
            return {}

    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("Checking dependencies...")

        missing_deps = []
        try:
            import PIL
            print("✓ Pillow (PIL) is installed")
        except ImportError:
            missing_deps.append("pillow")

        # Check optional dev dependencies if in dev mode
        if self.is_dev_mode():
            try:
                import black
                print("✓ Black (code formatter) is installed")
            except ImportError:
                print("⚠ Black (code formatter) not found - install with: pip install black")

            try:
                import flake8
                print("✓ Flake8 (linter) is installed")
            except ImportError:
                print("⚠ Flake8 (linter) not found - install with: pip install flake8")

            try:
                import pytest
                print("✓ Pytest (testing) is installed")
            except ImportError:
                print("⚠ Pytest (testing) not found - install with: pip install pytest")

        if missing_deps:
            print(f"\nMissing required dependencies: {', '.join(missing_deps)}")
            return False

        print("All required dependencies are installed.")
        return True

    def install_dependencies(self):
        """Install required dependencies"""
        print("Installing dependencies...")

        deps = []
        if 'dependencies' in self.config:
            deps.extend(self.config['dependencies'].keys())

        if deps:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + deps)
                print("Dependencies installed successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to install dependencies: {e}")
                return False
        else:
            print("No dependencies to install.")
            return True

    def install_dev_dependencies(self):
        """Install development dependencies"""
        print("Installing development dependencies...")

        deps = []
        if 'devDependencies' in self.config:
            deps.extend(self.config['devDependencies'].keys())

        if deps:
            try:
                subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + deps)
                print("Development dependencies installed successfully.")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Failed to install development dependencies: {e}")
                return False
        else:
            print("No development dependencies to install.")
            return True

    def check_python_version(self):
        """Check if Python version meets requirements"""
        if 'engines' in self.config and 'python' in self.config['engines']:
            required_version = self.config['engines']['python']
            current_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"

            print(f"Python version: {current_version}")
            print(f"Required version: {required_version}")

            # Simple version check (could be improved)
            if current_version.startswith(required_version.replace('>=', '')):
                print("✓ Python version is compatible.")
                return True
            else:
                print("✗ Python version does not meet requirements.")
                return False

        return True

    def create_shortcut(self):
        """Create desktop shortcut"""
        try:
            if platform.system() == "Windows":
                self._create_windows_shortcut()
            elif platform.system() == "Darwin":  # macOS
                self._create_macos_shortcut()
            else:  # Linux
                self._create_linux_shortcut()
            print("Desktop shortcut created successfully.")
            return True
        except Exception as e:
            print(f"Failed to create shortcut: {e}")
            return False

    def _create_windows_shortcut(self):
        """Create Windows shortcut"""
        try:
            import winshell
            from win32com.client import Dispatch

            desktop = winshell.desktop()
            shortcut_path = os.path.join(desktop, "FAF Explorer.lnk")

            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(shortcut_path)
            shortcut.Targetpath = str(self.project_root / "faf.py")
            shortcut.WorkingDirectory = str(self.project_root)
            shortcut.IconLocation = str(self.project_root / "ui" / "icon.ico") if (self.project_root / "ui" / "icon.ico").exists() else ""
            shortcut.save()

        except ImportError:
            print("pywin32 not available. Install with: pip install pywin32")
            # Fallback: create batch file
            desktop = os.path.join(os.environ['USERPROFILE'], 'Desktop')
            batch_path = os.path.join(desktop, "FAF Explorer.bat")
            with open(batch_path, 'w') as f:
                f.write(f'@echo off\ncd /d "{self.project_root}"\npython faf.py\npause')

    def _create_macos_shortcut(self):
        """Create macOS application shortcut"""
        # Create a simple shell script
        desktop = os.path.expanduser("~/Desktop")
        script_path = os.path.join(desktop, "FAF Explorer.command")
        with open(script_path, 'w') as f:
            f.write(f'#!/bin/bash\ncd "{self.project_root}"\npython3 faf.py')
        os.chmod(script_path, 0o755)

    def _create_linux_shortcut(self):
        """Create Linux desktop shortcut"""
        desktop = os.path.expanduser("~/Desktop")
        shortcut_path = os.path.join(desktop, "faf-explorer.desktop")

        with open(shortcut_path, 'w') as f:
            f.write(f"""[Desktop Entry]
Name=FAF Explorer
Comment={self.config.get('description', 'File and Folder Manager')}
Exec=python3 {self.project_root}/faf.py
Path={self.project_root}
Terminal=false
Type=Application
Categories=Utility;FileManager;
""")
        os.chmod(shortcut_path, 0o755)

    def check_for_updates(self):
        """Check for updates from repository"""
        if 'repository' not in self.config or 'url' not in self.config['repository']:
            print("No repository URL configured for updates.")
            return None

        repo_url = self.config['repository']['url']
        print(f"Checking for updates from: {repo_url}")

        try:
            # This is a simplified check - in reality you'd check tags/releases
            # For now, just check if we can connect
            import requests
            response = requests.get(repo_url.replace('.git', '/releases/latest'), timeout=10)
            if response.status_code == 200:
                latest_info = response.json()
                latest_version = latest_info.get('tag_name', '').lstrip('v')

                current_version = self.config.get('version', '0.0.0')

                if latest_version and latest_version != current_version:
                    print(f"Update available: {current_version} → {latest_version}")
                    return latest_version
                else:
                    print("You are running the latest version.")
                    return None
            else:
                print("Could not check for updates.")
                return None

        except ImportError:
            print("requests library not available for update checking.")
            return None
        except Exception as e:
            print(f"Error checking for updates: {e}")
            return None

    def update_project(self):
        """Update project to latest version"""
        latest_version = self.check_for_updates()
        if not latest_version:
            return False

        print(f"Updating to version {latest_version}...")

        try:
            # Use git to pull latest changes
            result = subprocess.run(['git', 'pull'], cwd=self.project_root,
                                  capture_output=True, text=True)

            if result.returncode == 0:
                print("Update completed successfully.")
                print("Please restart FAF Explorer.")
                return True
            else:
                print(f"Update failed: {result.stderr}")
                return False

        except FileNotFoundError:
            print("Git not found. Please update manually from the repository.")
            return False
        except Exception as e:
            print(f"Update failed: {e}")
            return False

    def run_diagnostics(self):
        """Run system diagnostics"""
        print("=== FAF Explorer Diagnostics ===\n")

        print(f"Project: {self.config.get('name', 'Unknown')}")
        print(f"Version: {self.config.get('version', 'Unknown')}")
        print(f"Python: {sys.version}")
        print(f"Platform: {platform.system()} {platform.release()}")
        print(f"Project Root: {self.project_root}")
        print()

        # Check Python version
        print("Checking Python version...")
        if self.check_python_version():
            print("✓ Python version OK")
        else:
            print("✗ Python version issue")
        print()

        # Check dependencies
        print("Checking dependencies...")
        if self.check_dependencies():
            print("✓ Dependencies OK")
        else:
            print("✗ Missing dependencies")
        print()

        # Check file structure
        print("Checking file structure...")
        required_files = ['faf.py', 'ui/gui.py', 'cli/main.py', 'core/__init__.py']
        missing_files = []

        for file_path in required_files:
            if not (self.project_root / file_path).exists():
                missing_files.append(file_path)

        if not missing_files:
            print("✓ File structure OK")
        else:
            print(f"✗ Missing files: {', '.join(missing_files)}")
        print()

        # Check permissions
        print("Checking permissions...")
        try:
            test_file = self.project_root / 'test_write.tmp'
            test_file.write_text('test')
            test_file.unlink()
            print("✓ Write permissions OK")
        except Exception as e:
            print(f"✗ Permission issue: {e}")
        print()

        print("=== Diagnostics Complete ===")

    def is_dev_mode(self):
        """Check if running in development mode"""
        return (self.project_root / '.git').exists()

    def get_system_info(self):
        """Get system information"""
        return {
            'python_version': sys.version,
            'platform': platform.system(),
            'platform_version': platform.release(),
            'architecture': platform.machine(),
            'project_root': str(self.project_root),
            'working_directory': os.getcwd()
        }


def main():
    """Main entry point for project manager"""
    import argparse

    parser = argparse.ArgumentParser(description="FAF Explorer Project Manager")
    parser.add_argument('command', choices=[
        'install', 'update', 'check-deps', 'diagnostics',
        'shortcut', 'info', 'version', 'build'
    ], help='Command to execute')

    args = parser.parse_args()

    pm = ProjectManager()

    if args.command == 'install':
        print("Installing FAF Explorer...")
        if pm.check_python_version() and pm.install_dependencies():
            print("Installation completed successfully!")
            if input("Create desktop shortcut? (y/N): ").lower().startswith('y'):
                pm.create_shortcut()
        else:
            print("Installation failed.")
            sys.exit(1)

    elif args.command == 'update':
        if pm.update_project():
            print("Update completed.")
        else:
            print("Update failed or not needed.")
            sys.exit(1)

    elif args.command == 'check-deps':
        if pm.check_dependencies():
            print("All dependencies are satisfied.")
        else:
            print("Missing dependencies. Run 'faf-pm install' to install them.")
            sys.exit(1)

    elif args.command == 'diagnostics':
        pm.run_diagnostics()

    elif args.command == 'shortcut':
        if pm.create_shortcut():
            print("Shortcut created successfully.")
        else:
            print("Failed to create shortcut.")
            sys.exit(1)

    elif args.command == 'build':
        print("Building FAF Explorer executable...")
        try:
            import subprocess
            result = subprocess.run([pm.project_root / 'build.py'], cwd=pm.project_root)
            if result.returncode == 0:
                print("Build completed successfully.")
            else:
                print("Build failed.")
                sys.exit(1)
        except Exception as e:
            print(f"Build error: {e}")
            sys.exit(1)

    elif args.command == 'info':
        info = pm.get_system_info()
        config = pm.config
        print(f"Project: {config.get('name', 'Unknown')}")
        print(f"Version: {config.get('version', 'Unknown')}")
        print(f"Description: {config.get('description', 'Unknown')}")
        print(f"Author: {config.get('author', 'Unknown')}")
        print(f"License: {config.get('license', 'Unknown')}")
        print(f"Python: {info['python_version'].split()[0]}")
        print(f"Platform: {info['platform']} {info['platform_version']}")
        print(f"Project Root: {info['project_root']}")

    elif args.command == 'version':
        print(pm.config.get('version', 'Unknown'))


if __name__ == "__main__":
    main()
