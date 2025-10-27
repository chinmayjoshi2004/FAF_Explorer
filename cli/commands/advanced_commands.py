from core import *
from cli.utils import print_success, print_error, print_warning, print_info


def search_files_cmd(args):
    """Search for files"""
    try:
        matches = search_files(
            args.path, args.query, args.recursive, args.case_sensitive
        )
        if isinstance(matches, list):
            if matches:
                print(f"Search Results for '{args.query}':")
                for match in matches:
                    print(match)
            else:
                print_info("No matches found")
        else:
            print_error(matches)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def index_files_cmd(args):
    """Index files for faster searching"""
    try:
        success, index_path = index_files(args.path, args.index_path)
        if success:
            print_success(f"Index created: {index_path}")
        else:
            print_error(index_path)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def set_permissions_cmd(args):
    """Set permissions"""
    try:
        success = set_permissions(args.path, args.permissions)
        if success:
            print_success("Permissions set")
        else:
            print_error("Failed to set permissions")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_permissions_cmd(args):
    """Get permissions"""
    try:
        perms = get_permissions(args.path)
        if perms:
            print(f"Permissions: {perms}")
        else:
            print_error("Failed to get permissions")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def encrypt_file_cmd(args):
    """Encrypt a file"""
    try:
        success, result = encrypt_file(args.path, args.password)
        if success:
            print_success(f"File encrypted: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def decrypt_file_cmd(args):
    """Decrypt a file"""
    try:
        success, result = decrypt_file(args.path, args.password)
        if success:
            print_success(f"File decrypted: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")
