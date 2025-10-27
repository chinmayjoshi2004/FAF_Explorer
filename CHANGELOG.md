# Changelog

All notable changes to FAF Explorer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-27

### Added

- **Graphical User Interface (GUI)**: Complete GUI implementation using Tkinter
  - Windows Explorer-style interface with ribbon toolbar
  - File tree view with lazy loading and expansion
  - Operations header with grouped buttons (Clipboard, Organize, New, Open)
  - Output panel for displaying file contents and operation logs
  - Status bar with real-time feedback
  - Context menus for right-click operations
  - Auto-display of supported text file formats
  - Search functionality with real-time filtering
  - Keyboard shortcuts support (Ctrl+N, Ctrl+Shift+N, Delete, F5, Ctrl+F)

- **GUI File Operations**:
  - Create new files and folders through GUI buttons
  - Delete files and folders with confirmation dialogs
  - Rename files and folders
  - Copy and paste files/folders with overwrite support
  - Move files/folders (cut and paste) with overwrite support
  - Open files with default system applications
  - Display file/folder properties

- **Enhanced Copy/Paste Functionality**:
  - Clipboard operations for files and folders
  - Overwrite confirmation dialogs
  - Proper clipboard state management
  - Support for both copy and move operations

- **GUI Enhancements**:
  - Professional styling with modern look and feel
  - Responsive layout with paned windows
  - Scrollbars for large content areas
  - Icon placeholders (using PIL for colored rectangles)
  - Error handling with user-friendly message boxes
  - Loading states and progress feedback

### Changed

- Updated version from 0.2.0 to 1.0.0 to reflect major GUI addition
- Enhanced project structure with dedicated `ui/` directory
- Improved user experience with intuitive GUI interface
- Maintained backward compatibility with existing CLI functionality

### Technical Details

- Added `ui/gui.py` with complete Tkinter-based GUI implementation
- Integrated core file/folder operations into GUI event handlers
- Added `if __name__ == "__main__"` block for direct GUI execution
- Implemented lazy loading for file tree to handle large directories efficiently
- Added proper event binding for keyboard shortcuts and mouse interactions
- Integrated PIL for icon generation (fallback to text-only if unavailable)

## [0.2.0] - 2025-10-27

### Added

- **Development Tools Integration**: Added comprehensive development tooling to the CLI
  - `faf dev format [path]` - Format code with Black (PEP 8 compliance)
  - `faf dev lint [path]` - Lint code with Flake8 (code quality analysis)
  - `faf --pytest` - Run pytest test suite directly from CLI
- **Code Quality Tools**: Integrated Black and Flake8 for automated code formatting and linting
- **Testing Integration**: Direct pytest execution support for streamlined development workflow

### Changed

- Enhanced CLI structure with new `dev` command group for development operations
- Updated requirements.txt to include Black and Flake8 dependencies
- Improved development workflow with integrated code quality tools

### Technical Details

- Added `cli/commands/dev_commands.py` module for development tool implementations
- Updated `cli/parsers.py` to include dev command subparsers
- Integrated subprocess execution for Black, Flake8, and pytest tools
- Added proper error handling for missing development dependencies
- Maintained backward compatibility with existing CLI functionality

## [0.1.0] - 2024-12-XX

### Added

- Initial release of FAF Explorer CLI
- Comprehensive file operations (create, read, write, delete, copy, move, rename)
- Folder operations (create, delete, list, copy, move, rename, size, duplicates)
- System operations (cwd, cd, path checks, disk usage, bookmarks, batch rename)
- Advanced operations (search, index, permissions, encryption/decryption)
- Modular CLI structure with separate command modules
- ANSI color-coded output for better user experience
- Comprehensive help system with examples
- Configuration support via JSON files

### Changed

- Replaced rich library dependencies with built-in Python features for better portability
- Refactored code into modular structure for maintainability

### Technical Details

- Removed external dependencies (rich library)
- Implemented custom color printing using ANSI escape codes
- Separated concerns into dedicated modules:
  - `cli/main.py`: Entry point
  - `cli/parsers.py`: Argument parsing setup
  - `cli/utils.py`: Utility functions
  - `cli/commands/`: Command implementations by category
- Added proper error handling and user confirmations
- Created professional .gitignore file
