from core import *
from cli.utils import print_success, print_error, print_warning, print_info


def get_cwd_cmd(args):
    """Get current working directory"""
    try:
        cwd = get_cwd()
        print_success(f"Current directory: {cwd}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def change_directory_cmd(args):
    """Change current working directory"""
    try:
        success, new_dir = change_directory(args.path)
        if success:
            print_success(f"Changed to: {new_dir}")
        else:
            print_error(new_dir)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def path_exists_cmd(args):
    """Check if path exists"""
    try:
        exists = path_exists(args.path)
        if exists:
            print_success(f"Path exists: {args.path}")
        else:
            print_info(f"Path does not exist: {args.path}")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_path_type_cmd(args):
    """Get path type"""
    try:
        path_type = get_path_type(args.path)
        if path_type in ["file", "folder"]:
            print_success(f"Path type: {path_type}")
        else:
            print_error(path_type)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_disk_usage_cmd(args):
    """Get disk usage"""
    try:
        usage = get_disk_usage(args.path)
        if isinstance(usage, dict):
            print("Disk Usage:")
            for key, value in usage.items():
                print(f"{key.title()}: {value} bytes")
        else:
            print_error(usage)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def create_bookmark_cmd(args):
    """Create a bookmark"""
    try:
        success = create_bookmark(args.path, args.name)
        if success:
            print_success(f"Bookmark created: {args.name}")
        else:
            print_error("Failed to create bookmark")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def list_bookmarks_cmd(args):
    """List bookmarks"""
    try:
        bookmarks = list_bookmarks()
        if bookmarks:
            print("Bookmarks:")
            for name, path in bookmarks.items():
                print(f"{name}: {path}")
        else:
            print_info("No bookmarks found")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def batch_rename_cmd(args):
    """Batch rename files"""
    try:
        success, renamed = batch_rename(args.paths, args.pattern)
        if success:
            print_success("Batch rename completed")
            for old, new in zip(args.paths, renamed):
                print(f"  {old} -> {new}")
        else:
            print_error(renamed)
    except Exception as e:
        print_error(f"Error: {str(e)}")
