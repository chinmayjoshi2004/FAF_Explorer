# Changelog

All notable changes to FAF Explorer will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
