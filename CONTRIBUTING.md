# Contributing to FAF Explorer

Thank you for your interest in contributing to FAF Explorer! We welcome contributions from the community. This document provides guidelines and information for contributors.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [How to Contribute](#how-to-contribute)
- [Development Guidelines](#development-guidelines)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Reporting Issues](#reporting-issues)

## Code of Conduct

This project adheres to a code of conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to the maintainers.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally:

   ```bash
   git clone https://github.com/chinmayjoshi2004/faf-explorer.git
   cd faf-explorer
   ```

3. Create a branch for your changes:

   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Setup

### Prerequisites

- Python 3.6 or higher
- Git

### Installation

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. (Optional) Set up a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

### Running the Application

```bash
python faf.py --help
```

## How to Contribute

### Types of Contributions

- **Bug fixes**: Fix existing issues
- **Features**: Add new functionality
- **Documentation**: Improve documentation
- **Tests**: Add or improve tests
- **Code style**: Improve code quality and consistency

### Finding Issues to Work On

- Check the [Issues](https://github.com/chinmayjoshi2004/faf-explorer/issues) page
- Look for issues labeled "good first issue" or "help wanted"
- Comment on an issue to indicate you're working on it

## Development Guidelines

### Code Style

- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions small and focused on a single responsibility

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Keep the first line under 50 characters
- Add more details in the body if needed

Example:

```bash
Add file compression feature

- Implement ZIP compression for files
- Add progress indication
- Update documentation
```

### Branch Naming

- Use descriptive branch names
- Prefix with the type of change:
  - `feature/` for new features
  - `bugfix/` for bug fixes
  - `docs/` for documentation
  - `refactor/` for code refactoring

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_file_operations.py

# Run with coverage
python -m pytest --cov=cli --cov-report=html
```

### Writing Tests

- Add tests for new features
- Ensure tests cover both success and failure cases
- Use descriptive test names
- Follow the existing test structure

## Submitting Changes

1. Ensure your code follows the development guidelines
2. Run tests and ensure they pass
3. Update documentation if needed
4. Commit your changes:

   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   ```

5. Push to your fork:

   ```bash
   git push origin feature/your-feature-name
   ```

6. Create a Pull Request on GitHub

### Pull Request Guidelines

- Provide a clear description of the changes
- Reference any related issues
- Include screenshots for UI changes
- Ensure CI checks pass
- Request review from maintainers

## Reporting Issues

### Bug Reports

When reporting bugs, please include:

- A clear title describing the issue
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- System information (OS, Python version)
- Error messages or stack traces

### Feature Requests

For feature requests, please include:

- A clear description of the proposed feature
- Use case or problem it solves
- Any relevant examples or mockups

## Additional Resources

- [Python Documentation](https://docs.python.org/3/)
- [PEP 8 Style Guide](https://pep8.org/)
- [Git Documentation](https://git-scm.com/doc)

Thank you for contributing to FAF Explorer!
