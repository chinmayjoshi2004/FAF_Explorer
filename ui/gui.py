#!/usr/bin/env python3
"""
FAF Explorer GUI - Main GUI Components
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import os
from pathlib import Path
import sys
import threading
import queue
from PIL import Image, ImageTk  # For icons

# Import logging
from faf_explorer.logger import get_logger

# Add parent directory to path to import core modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core import *

class FAFExplorerGUI:
    """Main GUI application class for FAF Explorer"""

    def __init__(self, root):
        # Initialize logger
        self.logger = get_logger("gui")

        self.root = root
        self.root.title("FAF Explorer - File and Folder Manager")
        self.root.geometry("1000x700")

        # Initialize variables
        self.current_path = Path.home()
        self.selected_item = None
        self.loading_queue = queue.Queue()
        self.loading_thread = None
        self.is_loading = False
        self.clipboard_item = None  # Path of copied/cut item
        self.clipboard_operation = None  # 'copy' or 'cut'

        # Load icons
        self.load_icons()

        # Create GUI components
        self.create_menu()
        self.create_toolbar()
        self.create_main_layout()
        self.create_status_bar()

        # Initialize file tree
        self.populate_file_tree()

        # Bind events
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.bind('<Control-n>', lambda e: self.new_file())
        self.root.bind('<Control-Shift-N>', lambda e: self.new_folder())
        self.root.bind('<Delete>', lambda e: self.delete_item())
        self.root.bind('<F5>', lambda e: self.refresh_tree())
        self.root.bind('<Control-f>', lambda e: self.focus_search())

        self.logger.info("FAF Explorer GUI initialized")

    def create_menu(self):
        """Create the main menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New File", command=self.new_file)
        file_menu.add_command(label="New Folder", command=self.new_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_closing)

        # Edit menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=edit_menu)
        edit_menu.add_command(label="Delete", command=self.delete_item)
        edit_menu.add_command(label="Rename", command=self.rename_item)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh", command=self.refresh_tree)
        view_menu.add_command(label="Go Home", command=self.go_home)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=2)

        # Navigation buttons with icons
        up_btn = ttk.Button(toolbar, image=self.up_icon, command=self.go_up)
        up_btn.pack(side=tk.LEFT, padx=2)
        home_btn = ttk.Button(toolbar, image=self.home_icon, command=self.go_home)
        home_btn.pack(side=tk.LEFT, padx=2)

        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Search entry
        ttk.Label(toolbar, text="Search:").pack(side=tk.LEFT, padx=2)
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(toolbar, textvariable=self.search_var, width=20)
        self.search_entry.pack(side=tk.LEFT, padx=2)
        self.search_entry.bind('<KeyRelease>', self.on_search)

        # Separator
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)

        # Path entry
        ttk.Label(toolbar, text="Path:").pack(side=tk.LEFT, padx=2)
        self.path_var = tk.StringVar(value=str(self.current_path))
        path_entry = ttk.Entry(toolbar, textvariable=self.path_var)
        path_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        path_entry.bind('<Return>', self.navigate_to_path)

        # Go button
        ttk.Button(toolbar, text="Go", command=self.navigate_to_path).pack(side=tk.LEFT, padx=2)

    def create_main_layout(self):
        """Create the main layout with operations header like Windows Explorer"""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Operations header (like Windows Explorer ribbon)
        self.create_operations_header(main_frame)

        # Create paned window below the header
        paned = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True)

        # Left panel - File tree
        left_frame = ttk.Frame(paned)
        paned.add(left_frame, weight=1)

        # Tree view
        tree_frame = ttk.Frame(left_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=("type", "size"))
        self.tree.heading('#0', text='Name')
        self.tree.heading('type', text='Type')
        self.tree.heading('size', text='Size')
        self.tree.column('type', width=100)
        self.tree.column('size', width=100)

        # Scrollbars
        tree_scroll_y = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        tree_scroll_x = ttk.Scrollbar(tree_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=tree_scroll_y.set, xscrollcommand=tree_scroll_x.set)

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tree_scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        tree_scroll_x.pack(side=tk.BOTTOM, fill=tk.X)

        # Bind events
        self.tree.bind('<<TreeviewSelect>>', self.on_tree_select)
        self.tree.bind('<Double-1>', self.on_tree_double_click)
        self.tree.bind('<<TreeviewOpen>>', self.on_tree_open)
        self.tree.bind('<Button-3>', self.on_tree_right_click)

        # Right panel - Output area only
        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=1)

        # Output area
        output_frame = ttk.Frame(right_frame)
        output_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(output_frame, text="Output:").pack(anchor=tk.W)
        self.output_text = scrolledtext.ScrolledText(output_frame, height=10)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def create_operations_header(self, parent):
        """Create operations header like Windows Explorer ribbon"""
        header_frame = ttk.Frame(parent, relief=tk.RAISED, borderwidth=1)
        header_frame.pack(fill=tk.X, padx=5, pady=(0,5))

        # Home tab (main operations)
        home_label = ttk.Label(header_frame, text="Home", font=("Arial", 10, "bold"))
        home_label.pack(side=tk.LEFT, padx=10, pady=5)

        # Clipboard group
        clipboard_frame = ttk.LabelFrame(header_frame, text="Clipboard", padding=5)
        clipboard_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(clipboard_frame, text="Copy", command=self.copy_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(clipboard_frame, text="Paste", command=self.paste_item).pack(side=tk.LEFT, padx=2)

        # Organize group
        organize_frame = ttk.LabelFrame(header_frame, text="Organize", padding=5)
        organize_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(organize_frame, text="Move", command=self.move_selected).pack(side=tk.LEFT, padx=2)
        ttk.Button(organize_frame, text="Delete", command=self.delete_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(organize_frame, text="Rename", command=self.rename_item).pack(side=tk.LEFT, padx=2)

        # New group
        new_frame = ttk.LabelFrame(header_frame, text="New", padding=5)
        new_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(new_frame, text="New File", command=self.new_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(new_frame, text="New Folder", command=self.new_folder).pack(side=tk.LEFT, padx=2)

        # Open group
        open_frame = ttk.LabelFrame(header_frame, text="Open", padding=5)
        open_frame.pack(side=tk.LEFT, padx=5, pady=5)

        ttk.Button(open_frame, text="Open", command=self.open_item).pack(side=tk.LEFT, padx=2)
        ttk.Button(open_frame, text="Properties", command=self.show_properties).pack(side=tk.LEFT, padx=2)

    def create_status_bar(self):
        """Create status bar"""
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def populate_file_tree(self):
        """Populate the file tree with lazy loading"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            self._add_directory_to_tree_lazy("", self.current_path)
            self.status_var.set(f"Loaded: {self.current_path}")
        except Exception as e:
            self.log_output(f"Error loading tree: {str(e)}")

    def _add_directory_to_tree_lazy(self, parent, path):
        """Add directory to tree lazily (only top level)"""
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith('.'):  # Skip hidden files
                    continue

                # Determine type and size
                if item.is_file():
                    item_type = "File"
                    try:
                        size = item.stat().st_size
                        size_str = f"{size} bytes"
                    except:
                        size_str = "Unknown"
                else:
                    item_type = "Folder"
                    size_str = ""

                # Add to tree
                node = self.tree.insert(parent, 'end', text=item.name,
                                      values=(item_type, size_str), open=False)

                # Add dummy child for directories to enable expansion
                if item.is_dir():
                    self.tree.insert(node, 'end', text='', values=('', ''), open=False)

        except PermissionError:
            pass  # Skip directories we can't access

    def on_tree_open(self, event):
        """Handle tree expansion (lazy loading)"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            item_text = self.tree.item(item, 'text')
            item_path = self.current_path / item_text

            if item_path.is_dir():
                # Clear dummy child
                for child in self.tree.get_children(item):
                    self.tree.delete(child)

                # Load actual children
                self._add_directory_to_tree_lazy(item, item_path)

    def on_tree_select(self, event):
        """Handle tree selection"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            item_text = self.tree.item(item, 'text')
            self.selected_item = self.current_path / item_text

            # Auto-display file content for supported formats
            if self.selected_item.is_file():
                self.display_file_content()
            else:
                # Clear output for folders
                self.output_text.delete(1.0, tk.END)

    def on_tree_double_click(self, event):
        """Handle double click"""
        selection = self.tree.selection()
        if selection:
            item = selection[0]
            item_text = self.tree.item(item, 'text')
            item_path = self.current_path / item_text

            if item_path.is_dir():
                self.current_path = item_path
                self.path_var.set(str(self.current_path))
                self.populate_file_tree()

    def navigate_to_path(self, event=None):
        """Navigate to entered path"""
        path_str = self.path_var.get()
        if os.path.exists(path_str):
            self.current_path = Path(path_str)
            self.populate_file_tree()
        else:
            messagebox.showerror("Error", "Path does not exist")

    def go_up(self):
        """Go to parent directory"""
        parent = self.current_path.parent
        if parent != self.current_path:
            self.current_path = parent
            self.path_var.set(str(self.current_path))
            self.populate_file_tree()

    def go_home(self):
        """Go to home directory"""
        self.current_path = Path.home()
        self.path_var.set(str(self.current_path))
        self.populate_file_tree()

    def refresh_tree(self):
        """Refresh the file tree"""
        self.populate_file_tree()

    def new_file(self):
        """Create new file"""
        from tkinter import simpledialog
        filename = simpledialog.askstring("New File", "Enter filename:")
        if filename:
            file_path = self.current_path / filename
            success, result = create_file(str(file_path))
            if success:
                self.refresh_tree()
                self.log_output(f"Created file: {result}")
            else:
                messagebox.showerror("Error", f"Failed to create file: {result}")

    def new_folder(self):
        """Create new folder"""
        from tkinter import simpledialog
        foldername = simpledialog.askstring("New Folder", "Enter folder name:")
        if foldername:
            folder_path = self.current_path / foldername
            success, result = create_folder(str(folder_path))
            if success:
                self.refresh_tree()
                self.log_output(f"Created folder: {result}")
            else:
                messagebox.showerror("Error", f"Failed to create folder: {result}")

    def read_file(self):
        """Read selected file"""
        if not self.selected_item or not self.selected_item.is_file():
            messagebox.showwarning("Warning", "Please select a file")
            return

        content = read_file(str(self.selected_item))
        if isinstance(content, str) and not content.startswith("File not found"):
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, content)
        else:
            messagebox.showerror("Error", f"Failed to read file: {content}")

    def write_file(self):
        """Write to selected file"""
        if not self.selected_item or not self.selected_item.is_file():
            messagebox.showwarning("Warning", "Please select a file")
            return

        from tkinter import simpledialog
        content = simpledialog.askstring("Write to File", "Enter content:")
        if content is not None:
            success, result = write_file(str(self.selected_item), content)
            if success:
                self.log_output(f"Written {result} bytes to file")
            else:
                messagebox.showerror("Error", f"Failed to write file: {result}")

    def list_folder(self):
        """List folder contents"""
        if not self.selected_item or not self.selected_item.is_dir():
            folder_path = self.current_path
        else:
            folder_path = self.selected_item

        contents = list_folder(str(folder_path))
        if isinstance(contents, list):
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"Contents of {folder_path}:\n\n")
            self.output_text.insert(tk.END, "\n".join(contents))
        else:
            messagebox.showerror("Error", f"Failed to list folder: {contents}")

    def delete_item(self):
        """Delete selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return

        if messagebox.askyesno("Confirm", f"Delete {self.selected_item.name}?"):
            if self.selected_item.is_file():
                success, result = delete_file(str(self.selected_item))
            else:
                success, result = delete_folder(str(self.selected_item))
            if success:
                self.refresh_tree()
                self.log_output(f"Deleted: {self.selected_item.name}")
            else:
                messagebox.showerror("Error", f"Failed to delete: {result}")

    def rename_item(self):
        """Rename selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return

        from tkinter import simpledialog
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            success, result = rename_file(str(self.selected_item), new_name) if self.selected_item.is_file() else rename_folder(str(self.selected_item), new_name)
            if success:
                self.refresh_tree()
                self.log_output(f"Renamed to: {result}")
            else:
                messagebox.showerror("Error", f"Failed to rename: {result}")

    def log_output(self, message):
        """Log message to output"""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)

    def load_icons(self):
        """Load icons for toolbar buttons"""
        try:
            # Create simple icons using PIL
            self.up_icon = ImageTk.PhotoImage(Image.new('RGB', (16, 16), color='lightblue'))
            self.home_icon = ImageTk.PhotoImage(Image.new('RGB', (16, 16), color='lightgreen'))
        except ImportError:
            # Fallback if PIL is not available
            self.up_icon = None
            self.home_icon = None

    def focus_search(self):
        """Focus on search entry"""
        self.search_entry.focus_set()

    def on_search(self, event=None):
        """Handle search functionality"""
        search_term = self.search_var.get().lower()
        if not search_term:
            self.populate_file_tree()
            return

        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        try:
            for item in sorted(self.current_path.iterdir()):
                if item.name.startswith('.'):  # Skip hidden files
                    continue

                if search_term in item.name.lower():
                    # Determine type and size
                    if item.is_file():
                        item_type = "File"
                        try:
                            size = item.stat().st_size
                            size_str = f"{size} bytes"
                        except:
                            size_str = "Unknown"
                    else:
                        item_type = "Folder"
                        size_str = ""

                    # Add to tree
                    self.tree.insert("", 'end', text=item.name,
                                   values=(item_type, size_str), open=False)

            self.status_var.set(f"Search results for: {search_term}")
        except Exception as e:
            self.log_output(f"Error during search: {str(e)}")

    def on_tree_right_click(self, event):
        """Handle right-click context menu"""
        # Identify the item under the cursor
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            item_text = self.tree.item(item, 'text')
            self.selected_item = self.current_path / item_text

            # Create context menu
            context_menu = tk.Menu(self.root, tearoff=0)
            context_menu.add_command(label="Open", command=self.open_item)
            context_menu.add_separator()
            context_menu.add_command(label="Delete", command=self.delete_item)
            context_menu.add_command(label="Rename", command=self.rename_item)

            # Show context menu
            context_menu.post(event.x_root, event.y_root)

    def open_item(self):
        """Open selected item (file or folder)"""
        if not self.selected_item:
            return

        if self.selected_item.is_dir():
            self.current_path = self.selected_item
            self.path_var.set(str(self.current_path))
            self.populate_file_tree()
        else:
            # For files, try to open with default application
            try:
                import subprocess
                import platform
                if platform.system() == "Windows":
                    subprocess.run(["start", str(self.selected_item)], shell=True)
                elif platform.system() == "Darwin":  # macOS
                    subprocess.run(["open", str(self.selected_item)])
                else:  # Linux
                    subprocess.run(["xdg-open", str(self.selected_item)])
            except Exception as e:
                messagebox.showerror("Error", f"Could not open file: {str(e)}")

    def copy_selected(self):
        """Copy selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return

        self.clipboard_item = self.selected_item
        self.clipboard_operation = 'copy'
        self.status_var.set(f"Copied: {self.selected_item.name}")
        self.log_output(f"Copied: {self.selected_item.name}")

    def move_selected(self):
        """Move selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return

        self.clipboard_item = self.selected_item
        self.clipboard_operation = 'cut'
        self.status_var.set(f"Cut: {self.selected_item.name}")
        self.log_output(f"Cut: {self.selected_item.name}")

    def paste_item(self):
        """Paste item"""
        if not self.clipboard_item or not self.clipboard_operation:
            messagebox.showwarning("Warning", "Nothing to paste")
            return

        # Determine destination path
        destination = self.current_path / self.clipboard_item.name

        # Check if destination already exists
        if destination.exists():
            if not messagebox.askyesno("Confirm", f"Destination '{destination.name}' already exists. Overwrite?"):
                return

        try:
            if self.clipboard_operation == 'copy':
                if self.clipboard_item.is_file():
                    success, result = copy_file(str(self.clipboard_item), str(destination), overwrite=True)
                else:
                    success, result = copy_folder(str(self.clipboard_item), str(destination), overwrite=True)
                operation_name = "Copied"
            else:  # 'cut' operation
                if self.clipboard_item.is_file():
                    success, result = move_file(str(self.clipboard_item), str(destination), overwrite=True)
                else:
                    success, result = move_folder(str(self.clipboard_item), str(destination), overwrite=True)
                operation_name = "Moved"
                # Clear clipboard after move
                self.clipboard_item = None
                self.clipboard_operation = None

            if success:
                self.refresh_tree()
                self.status_var.set(f"{operation_name}: {destination.name}")
                self.log_output(f"{operation_name}: {destination.name}")
            else:
                messagebox.showerror("Error", f"Failed to {self.clipboard_operation}: {result}")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to {self.clipboard_operation}: {str(e)}")

    def show_properties(self):
        """Show properties of selected item"""
        if not self.selected_item:
            messagebox.showwarning("Warning", "Please select an item")
            return

        # Get file/folder properties
        try:
            stat_info = self.selected_item.stat()
            properties = f"Name: {self.selected_item.name}\n"
            properties += f"Path: {self.selected_item}\n"
            properties += f"Type: {'File' if self.selected_item.is_file() else 'Folder'}\n"
            properties += f"Size: {stat_info.st_size} bytes\n"
            properties += f"Modified: {stat_info.st_mtime}\n"
            properties += f"Permissions: {oct(stat_info.st_mode)[-3:]}"

            messagebox.showinfo("Properties", properties)
        except Exception as e:
            messagebox.showerror("Error", f"Could not get properties: {str(e)}")

    def display_file_content(self):
        """Display content of selected file if it's a supported text format"""
        if not self.selected_item or not self.selected_item.is_file():
            return

        # Check if file extension is supported for text display
        supported_extensions = {'.txt', '.py', '.md', '.json', '.xml', '.html', '.css', '.js', '.log', '.ini', '.cfg', '.yml', '.yaml'}
        file_extension = self.selected_item.suffix.lower()

        if file_extension in supported_extensions:
            try:
                # Read file content
                with open(self.selected_item, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()

                # Clear and display content
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Content of {self.selected_item.name}:\n\n")
                self.output_text.insert(tk.END, content)

            except Exception as e:
                self.output_text.delete(1.0, tk.END)
                self.output_text.insert(tk.END, f"Error reading file: {str(e)}")
        else:
            # For unsupported formats, show file info
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, f"File: {self.selected_item.name}\n")
            self.output_text.insert(tk.END, f"Type: {file_extension.upper()} file\n")
            self.output_text.insert(tk.END, "Content preview not supported for this file type.\n")
            self.output_text.insert(tk.END, "Use 'Open' button to view with default application.")

    def show_about(self):
        """Show about dialog"""
        messagebox.showinfo("About", "FAF Explorer v1.0.0\nFile and Folder Manager\n\nA powerful dual-interface file management tool\nwith both CLI and GUI capabilities.")

    def on_closing(self):
        """Handle application closing"""
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = FAFExplorerGUI(root)
    root.mainloop()
