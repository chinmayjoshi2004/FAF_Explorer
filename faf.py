#!/usr/bin/env python3
"""
FAF Explorer - Entry Point
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import and run the main application
from faf_explorer.main import main_entry

if __name__ == "__main__":
    main_entry()
