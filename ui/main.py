#!/usr/bin/env python3
"""
FAF Explorer GUI - Main GUI Application
"""

import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ui.gui import FAFExplorerGUI

def main():
    """Main GUI application entry point"""
    try:
        root = tk.Tk()
        app = FAFExplorerGUI(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start GUI: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
