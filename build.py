#!/usr/bin/env python3
"""
Build script for FAF Explorer - Creates standalone executables
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def check_pyinstaller():
    """Check if PyInstaller is installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller is installed")
        return True
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("✓ PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("✗ Failed to install PyInstaller")
            return False


def build_executable():
    """Build standalone executable using PyInstaller"""
    print("Building FAF Explorer executable...")

    project_root = Path(__file__).parent
    dist_dir = project_root / 'dist'
    build_dir = project_root / 'build'

    # Clean previous builds
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)

    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',  # Single executable file
        '--windowed',  # No console window for GUI
        '--name', 'FAF_Explorer',
        '--icon', str(project_root / 'ui' / 'icon.ico') if (project_root / 'ui' / 'icon.ico').exists() else None,
        '--add-data', f'{project_root / "config"};config',  # Include config directory
        '--hidden-import', 'PIL',  # Hidden imports
        '--hidden-import', 'tkinter',
        str(project_root / 'faf.py')  # Main script
    ]

    # Remove None values
    cmd = [arg for arg in cmd if arg is not None]

    try:
        result = subprocess.run(cmd, cwd=project_root, capture_output=True, text=True)

        if result.returncode == 0:
            print("✓ Executable built successfully!")
            exe_path = dist_dir / 'FAF_Explorer.exe' if os.name == 'nt' else dist_dir / 'FAF_Explorer'
            print(f"Executable location: {exe_path}")

            # Create installer if on Windows
            if os.name == 'nt':
                create_windows_installer(exe_path)

            return True
        else:
            print("✗ Build failed:")
            print(result.stdout)
            print(result.stderr)
            return False

    except Exception as e:
        print(f"✗ Build error: {e}")
        return False


def create_windows_installer(exe_path):
    """Create Windows installer using NSIS or Inno Setup if available"""
    print("Creating Windows installer...")

    try:
        # Try NSIS first
        nsis_script = create_nsis_script(exe_path)
        if nsis_script:
            result = subprocess.run(['makensis', nsis_script], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Windows installer created with NSIS")
                return True

        # Fallback: Try Inno Setup
        iss_script = create_inno_script(exe_path)
        if iss_script:
            result = subprocess.run(['iscc', iss_script], capture_output=True, text=True)
            if result.returncode == 0:
                print("✓ Windows installer created with Inno Setup")
                return True

        print("⚠ No installer tool found. Executable is ready for manual distribution.")
        return False

    except Exception as e:
        print(f"⚠ Installer creation failed: {e}")
        return False


def create_nsis_script(exe_path):
    """Create NSIS script for Windows installer"""
    try:
        import tempfile
        script_content = f"""
!include "MUI2.nsh"

Name "FAF Explorer"
OutFile "FAF_Explorer_Installer.exe"
InstallDir "$PROGRAMFILES\\FAF Explorer"
InstallDirRegKey HKCU "Software\\FAF Explorer" ""

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_DIRECTORY
!insertmacro MUI_PAGE_INSTFILES
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_WELCOME
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

!insertmacro MUI_LANGUAGE "English"

Section "Install"
    SetOutPath "$INSTDIR"
    File "{exe_path}"

    # Create desktop shortcut
    CreateShortCut "$DESKTOP\\FAF Explorer.lnk" "$INSTDIR\\FAF_Explorer.exe"

    # Registry entries
    WriteRegStr HKCU "Software\\FAF Explorer" "" $INSTDIR
    WriteUninstaller "$INSTDIR\\Uninstall.exe"
SectionEnd

Section "Uninstall"
    Delete "$INSTDIR\\FAF_Explorer.exe"
    Delete "$INSTDIR\\Uninstall.exe"
    Delete "$DESKTOP\\FAF Explorer.lnk"
    RMDir "$INSTDIR"
    DeleteRegKey HKCU "Software\\FAF Explorer"
SectionEnd
"""

        script_file = tempfile.NamedTemporaryFile(mode='w', suffix='.nsi', delete=False)
        script_file.write(script_content)
        script_file.close()
        return script_file.name

    except Exception:
        return None


def create_inno_script(exe_path):
    """Create Inno Setup script for Windows installer"""
    try:
        import tempfile
        script_content = f"""
#define MyAppName "FAF Explorer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "chinmayjoshi2004"
#define MyAppExeName "FAF_Explorer.exe"

[Setup]
AppId={{#MyAppName}}
AppName={{#MyAppName}}
AppVersion={{#MyAppVersion}}
AppPublisher={{#MyAppPublisher}}
DefaultDirName={{pf}}\\{{#MyAppName}}
DefaultGroupName={{#MyAppName}}
OutputDir=userdocs
OutputBaseFilename=FAF_Explorer_Installer
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{{cm:CreateDesktopIcon}}"; GroupDescription: "{{cm:AdditionalIcons}}"

[Files]
Source: "{exe_path}"; DestDir: "{{app}}"; Flags: ignoreversion

[Icons]
Name: "{{group}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"
Name: "{{commondesktop}}\\{{#MyAppName}}"; Filename: "{{app}}\\{{#MyAppExeName}}"; Tasks: desktopicon

[Run]
Filename: "{{app}}\\{{#MyAppExeName}}"; Description: "{{cm:LaunchProgram,{{#StringChange(MyAppName,'&','&&')}}}}"; Flags: nowait postinstall skipifsilent
"""

        script_file = tempfile.NamedTemporaryFile(mode='w', suffix='.iss', delete=False)
        script_file.write(script_content)
        script_file.close()
        return script_file.name

    except Exception:
        return None


def main():
    """Main build function"""
    print("FAF Explorer Build Script")
    print("=" * 30)

    if not check_pyinstaller():
        print("Cannot proceed without PyInstaller.")
        sys.exit(1)

    if build_executable():
        print("\nBuild completed successfully!")
        print("Check the 'dist' directory for the executable.")
    else:
        print("\nBuild failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
