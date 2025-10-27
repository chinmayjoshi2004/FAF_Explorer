from core import *
from cli.utils import print_success, print_error, print_warning, print_info


def create_folder_cmd(args):
    """Create a new folder"""
    try:
        success, result = create_folder(args.path, args.parents)
        if success:
            print_success(f"Folder created: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def delete_folder_cmd(args):
    """Delete a folder"""
    try:
        if not args.force:
            response = (
                input(f"Are you sure you want to delete {args.path}? (y/N): ")
                .strip()
                .lower()
            )
            if response not in ["y", "yes"]:
                return
        success = delete_folder(args.path, args.recursive, args.force)
        if success:
            print_success(f"Folder deleted: {args.path}")
        else:
            print_error(success)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def list_folder_cmd(args):
    """List folder contents"""
    try:
        items = list_folder(args.path, args.recursive, args.include_hidden, args.filter)
        if isinstance(items, list):
            if items:
                print(f"Contents of {args.path}:")
                for item in items:
                    print(item)
            else:
                print_info("Folder is empty")
        else:
            print_error(items)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def copy_folder_cmd(args):
    """Copy a folder"""
    try:
        success, result = copy_folder(
            args.source, args.destination, args.recursive, args.overwrite
        )
        if success:
            print_success(f"Folder copied to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def move_folder_cmd(args):
    """Move a folder"""
    try:
        success, result = move_folder(args.source, args.destination, args.overwrite)
        if success:
            print_success(f"Folder moved to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_folder_info_cmd(args):
    """Get folder information"""
    try:
        info = get_folder_info(args.path)
        if isinstance(info, dict):
            print(f"Folder Info: {args.path}")
            for key, value in info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print_error(info)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def rename_folder_cmd(args):
    """Rename a folder"""
    try:
        success, result = rename_folder(args.path, args.new_name)
        if success:
            print_success(f"Folder renamed to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def compress_folder_cmd(args):
    """Compress a folder"""
    try:
        success, result = compress_folder(args.path, args.archive_path, args.format)
        if success:
            print_success(f"Folder compressed to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_folder_size_cmd(args):
    """Get folder size"""
    try:
        size = get_folder_size(args.path)
        if isinstance(size, int):
            print_success(f"Folder size: {size} bytes")
        else:
            print_error(size)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def find_duplicates_cmd(args):
    """Find duplicate files in folder"""
    try:
        duplicates = find_duplicates(args.path, args.recursive)
        if isinstance(duplicates, list):
            if duplicates:
                for i, group in enumerate(duplicates):
                    print(f"Duplicate Group {i+1}:")
                    for file in group:
                        print(f"  {file}")
                    print()
            else:
                print_success("No duplicates found")
        else:
            print_error(duplicates)
    except Exception as e:
        print_error(f"Error: {str(e)}")
