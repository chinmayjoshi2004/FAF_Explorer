from core import *
from cli.utils import print_success, print_error, print_warning, print_info


def create_file_cmd(args):
    """Create a new file"""
    try:
        success, result = create_file(args.path, args.content, args.overwrite)
        if success:
            print_success(f"File created: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def read_file_cmd(args):
    """Read file contents"""
    try:
        content = read_file(args.path, args.encoding)
        if isinstance(content, str) and not content.startswith("File not found"):
            print(f"Contents of {args.path}:")
            print(content)
        else:
            print_error(content)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def write_file_cmd(args):
    """Write content to file"""
    try:
        success, bytes_written = write_file(
            args.path, args.content, args.mode, args.encoding
        )
        if success:
            print_success(f"Written {bytes_written} bytes to {args.path}")
        else:
            print_error(bytes_written)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def delete_file_cmd(args):
    """Delete a file"""
    try:
        if not args.force:
            response = (
                input(f"Are you sure you want to delete {args.path}? (y/N): ")
                .strip()
                .lower()
            )
            if response not in ["y", "yes"]:
                return
        success = delete_file(args.path, args.force)
        if success:
            print_success(f"File deleted: {args.path}")
        else:
            print_error(success)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def copy_file_cmd(args):
    """Copy a file"""
    try:
        success, result = copy_file(args.source, args.destination, args.overwrite)
        if success:
            print_success(f"File copied to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def move_file_cmd(args):
    """Move a file"""
    try:
        success, result = move_file(args.source, args.destination, args.overwrite)
        if success:
            print_success(f"File moved to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_file_info_cmd(args):
    """Get file information"""
    try:
        info = get_file_info(args.path)
        if isinstance(info, dict):
            print(f"File Info: {args.path}")
            for key, value in info.items():
                print(f"{key.replace('_', ' ').title()}: {value}")
        else:
            print_error(info)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def rename_file_cmd(args):
    """Rename a file"""
    try:
        success, result = rename_file(args.path, args.new_name)
        if success:
            print_success(f"File renamed to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def compress_file_cmd(args):
    """Compress a file"""
    try:
        success, result = compress_file(args.path, args.archive_path, args.format)
        if success:
            print_success(f"File compressed to: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def decompress_file_cmd(args):
    """Decompress an archive"""
    try:
        success, files = decompress_file(args.archive_path, args.destination)
        if success:
            print_success(f"Archive decompressed. Files: {', '.join(files)}")
        else:
            print_error(files)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def create_symlink_cmd(args):
    """Create a symbolic link"""
    try:
        success, result = create_symlink(args.target, args.link)
        if success:
            print_success(f"Symlink created: {result}")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def get_file_hash_cmd(args):
    """Get file hash"""
    try:
        hash_value = get_file_hash(args.path, args.algorithm)
        if hash_value:
            print(f"{args.algorithm.upper()} Hash: {hash_value}")
        else:
            print_error("Failed to calculate hash")
    except Exception as e:
        print_error(f"Error: {str(e)}")


def compare_files_cmd(args):
    """Compare two files"""
    try:
        result = compare_files(args.path1, args.path2)
        if result == "identical":
            print_success("Files are identical")
        elif result == "differences":
            print_warning("Files have differences")
        else:
            print_error(result)
    except Exception as e:
        print_error(f"Error: {str(e)}")


def set_file_attributes_cmd(args):
    """Set file attributes"""
    try:
        success = set_file_attributes(args.path, args.attributes)
        if success:
            print_success("File attributes set")
        else:
            print_error("Failed to set attributes")
    except Exception as e:
        print_error(f"Error: {str(e)}")
