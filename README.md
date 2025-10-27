# FAF Explorer

FAF Explorer is a powerful and user-friendly Command Line Interface (CLI) tool designed for comprehensive file and folder management. It provides a wide range of operations including file manipulation, folder handling, system utilities, and advanced features like searching, indexing, encryption, and more.

## Features

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

### Prerequisites

- Python 3.6 or higher
- Required Python packages (install via pip):

  ```bash
  pip install -r requirements.txt
  ```

### Installation Steps

1. Clone the repository:

   ```bash
   git clone https://github.com/chinmayjoshi2004/faf-explorer.git
   cd faf-explorer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Add to PATH for global access:

   ```bash
   # On Linux/Mac
   sudo ln -s $(pwd)/faf.py /usr/local/bin/faf

   # On Windows
   # Add the directory to your PATH environment variable
   ```

## Usage

### Basic Syntax

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
