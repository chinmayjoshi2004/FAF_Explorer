#!/usr/bin/env python3
"""
FAF Explorer Project Manager CLI
"""

import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from faf_explorer.project_manager import main

if __name__ == "__main__":
    main()
