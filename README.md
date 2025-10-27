# FAF Explorer

FAF Explorer is a powerful and user-friendly file and folder management tool that provides both a Command Line Interface (CLI) and a Graphical User Interface (GUI). It offers comprehensive operations including file manipulation, folder handling, system utilities, and advanced features like searching, indexing, encryption, and more.

**Version 1.0.0** - Now with full GUI support!

## Features

### Graphical User Interface (GUI)

- **Windows Explorer-style Interface**: Modern ribbon toolbar with grouped operations
- **File Tree View**: Lazy-loading tree with expansion, icons, and metadata display
- **Operations Header**: Clipboard, Organize, New, and Open operation groups
- **Output Panel**: Real-time display of file contents and operation logs
- **Search Functionality**: Real-time filtering of files and folders
- **Context Menus**: Right-click menus for quick operations
- **Keyboard Shortcuts**: Full keyboard support (Ctrl+N, Ctrl+Shift+N, Delete, F5, Ctrl+F)
- **Auto File Preview**: Automatic display of supported text file formats

### File Operations

- Create, read, write, delete files
- Copy, move, rename files
- Compress and decompress files
- Create symbolic links
- Calculate file hashes (MD5, SHA1, SHA256)
- Compare files
- Set file attributes

### Folder Operations

- Create, delete, list folders
- Copy, move, rename folders
- Get folder information and size
- Find duplicate files
- Compress folders

### System Operations

- Get/change current working directory
- Check path existence and type
- Get disk usage
- Manage bookmarks
- Batch rename files

### Advanced Operations

- Search for files with regex support
- Index files for faster searching
- Set and get file permissions
- Encrypt and decrypt files

### Development Tools

- **Code Formatting**: `faf dev format [path]` - Format code with Black for PEP 8 compliance
- **Code Linting**: `faf dev lint [path]` - Lint code with Flake8 for quality analysis
- **Testing**: `faf --pytest` - Run pytest test suite directly from CLI
- **Integrated Workflow**: Streamlined development with built-in code quality tools

## Installation

### Standalone Software (Recommended)

FAF Explorer is designed as standalone software, not a pip package. Download and run it directly:

#### Option 1: Download Pre-built Executable

- Visit the [Releases](https://github.com/chinmayjoshi2004/faf-explorer/releases) page
- Download the executable for your platform (Windows `.exe`, macOS `.app`, Linux binary)
- Run the executable directly - no installation required!

#### Option 2: Build from Source

1. Clone the repository:

   ```bash
   git clone https://github.com/chinmayjoshi2004/faf-explorer.git
   cd faf-explorer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Build the executable:

   ```bash
   python faf-pm.py build
   ```

   The executable will be created in the `dist/` directory.

4. Run the executable:

   ```bash
   # On Windows
   dist/FAF_Explorer.exe

   # On Linux/macOS
   ./dist/FAF_Explorer
   ```

#### Option 3: Run from Source (Development)

1. Clone the repository:

   ```bash
   git clone https://github.com/chinmayjoshi2004/faf-explorer.git
   cd faf-explorer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run directly:

   ```bash
   python faf.py
   ```

### Project Management

FAF Explorer includes a built-in project manager for installation, updates, and maintenance:

```bash
# Check system compatibility
python faf-pm.py diagnostics

# Install dependencies
python faf-pm.py install

# Check for updates
python faf-pm.py update

# Build executable
python faf-pm.py build

# Create desktop shortcut
python faf-pm.py shortcut

# Get project information
python faf-pm.py info
```

### Prerequisites

- Python 3.6 or higher (for building from source)
- Required Python packages (install via pip):

  ```bash
  pip install -r requirements.txt
  ```

## Usage

### Graphical User Interface

To launch the GUI version of FAF Explorer:

```bash
cd ui
python gui.py
```

The GUI provides an intuitive Windows Explorer-style interface with:

- File tree navigation on the left
- Operations ribbon at the top
- Output panel on the right for file previews and logs
- Status bar with real-time feedback

### Command Line Interface

#### Basic Syntax

```bash
faf <command> <subcommand> [options] [arguments]
```

### Examples

#### File Operations

```bash
# Create a new file
faf file create example.txt --content "Hello, World!"

# Read a file
faf file read example.txt

# Copy a file
faf file copy source.txt destination.txt

# Get file information
faf file info example.txt
```

#### Folder Operations

```bash
# List folder contents
faf folder list .

# Create a new folder
faf folder create new_folder

# Get folder size
faf folder size .
```

#### System Operations

```bash
# Get current directory
faf system cwd

# Change directory
faf system cd /path/to/directory

# Create a bookmark
faf system bookmark-create /important/path mybookmark
```

#### Advanced Operations

```bash
# Search for files
faf advanced search . "*.txt" --recursive

# Encrypt a file
faf advanced encrypt secret.txt --password mypassword

# Set permissions
faf advanced perm-set file.txt 755
```

#### Development Tools

```bash
# Format code with Black
faf dev format

# Lint code with Flake8
faf dev lint

# Run tests with pytest
faf --pytest
```

### Getting Help

```bash
# General help
faf --help

# Command-specific help
faf file --help
faf folder --help
faf system --help
faf advanced --help
faf dev --help
```

## Configuration

FAF Explorer uses a configuration file located at `config/operations.json` for storing settings and operation definitions. You can modify this file to customize behavior or add new operations.

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on how to get started.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a list of changes and version history.

## Support

If you encounter any issues or have questions:

- Check the [Issues](https://github.com/chinmayjoshi2004/faf-explorer/issues) page
- Read the documentation
- Contact the maintainers

## Authors

- chinmayjoshi2004 - Initial work

## Acknowledgments

- Thanks to all contributors
- Inspired by various file management tools
