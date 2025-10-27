import argparse
from cli.commands.file_commands import *
from cli.commands.folder_commands import *
from cli.commands.system_commands import *
from cli.commands.advanced_commands import *
from cli.commands.dev_commands import *


def setup_parsers():
    parser = argparse.ArgumentParser(
        description="FAF Explorer - File and Folder Explorer CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  faf file create test.txt --content "Hello World"
  faf file read test.txt
  faf folder list .
  faf search files . "test" --recursive
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # File operations
    file_parser = subparsers.add_parser("file", help="File operations")
    file_subparsers = file_parser.add_subparsers(
        dest="subcommand", help="File subcommands"
    )

    # File create
    create_parser = file_subparsers.add_parser("create", help="Create a new file")
    create_parser.add_argument("path", help="File path")
    create_parser.add_argument("--content", default="", help="File content")
    create_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite if exists"
    )
    create_parser.set_defaults(func=create_file_cmd)

    # File read
    read_parser = file_subparsers.add_parser("read", help="Read file contents")
    read_parser.add_argument("path", help="File path")
    read_parser.add_argument("--encoding", help="File encoding")
    read_parser.set_defaults(func=read_file_cmd)

    # File write
    write_parser = file_subparsers.add_parser("write", help="Write to file")
    write_parser.add_argument("path", help="File path")
    write_parser.add_argument("content", help="Content to write")
    write_parser.add_argument(
        "--mode", choices=["w", "a"], default="w", help="Write mode"
    )
    write_parser.add_argument("--encoding", help="File encoding")
    write_parser.set_defaults(func=write_file_cmd)

    # File delete
    delete_parser = file_subparsers.add_parser("delete", help="Delete a file")
    delete_parser.add_argument("path", help="File path")
    delete_parser.add_argument("--force", action="store_true", help="Force deletion")
    delete_parser.set_defaults(func=delete_file_cmd)

    # File copy
    copy_parser = file_subparsers.add_parser("copy", help="Copy a file")
    copy_parser.add_argument("source", help="Source path")
    copy_parser.add_argument("destination", help="Destination path")
    copy_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite destination"
    )
    copy_parser.set_defaults(func=copy_file_cmd)

    # File move
    move_parser = file_subparsers.add_parser("move", help="Move a file")
    move_parser.add_argument("source", help="Source path")
    move_parser.add_argument("destination", help="Destination path")
    move_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite destination"
    )
    move_parser.set_defaults(func=move_file_cmd)

    # File info
    info_parser = file_subparsers.add_parser("info", help="Get file information")
    info_parser.add_argument("path", help="File path")
    info_parser.set_defaults(func=get_file_info_cmd)

    # File rename
    rename_parser = file_subparsers.add_parser("rename", help="Rename a file")
    rename_parser.add_argument("path", help="File path")
    rename_parser.add_argument("new_name", help="New name")
    rename_parser.set_defaults(func=rename_file_cmd)

    # File compress
    compress_parser = file_subparsers.add_parser("compress", help="Compress a file")
    compress_parser.add_argument("path", help="File path")
    compress_parser.add_argument("archive_path", help="Archive path")
    compress_parser.add_argument(
        "--format", choices=["zip", "tar", "gz"], default="zip", help="Archive format"
    )
    compress_parser.set_defaults(func=compress_file_cmd)

    # File decompress
    decompress_parser = file_subparsers.add_parser(
        "decompress", help="Decompress an archive"
    )
    decompress_parser.add_argument("archive_path", help="Archive path")
    decompress_parser.add_argument("destination", help="Destination directory")
    decompress_parser.set_defaults(func=decompress_file_cmd)

    # File symlink
    symlink_parser = file_subparsers.add_parser("symlink", help="Create symbolic link")
    symlink_parser.add_argument("target", help="Target path")
    symlink_parser.add_argument("link", help="Link path")
    symlink_parser.set_defaults(func=create_symlink_cmd)

    # File hash
    hash_parser = file_subparsers.add_parser("hash", help="Get file hash")
    hash_parser.add_argument("path", help="File path")
    hash_parser.add_argument(
        "--algorithm",
        choices=["md5", "sha1", "sha256"],
        default="sha256",
        help="Hash algorithm",
    )
    hash_parser.set_defaults(func=get_file_hash_cmd)

    # File compare
    compare_parser = file_subparsers.add_parser("compare", help="Compare two files")
    compare_parser.add_argument("path1", help="First file path")
    compare_parser.add_argument("path2", help="Second file path")
    compare_parser.set_defaults(func=compare_files_cmd)

    # File attributes
    attr_parser = file_subparsers.add_parser("attributes", help="Set file attributes")
    attr_parser.add_argument("path", help="File path")
    attr_parser.add_argument("--attributes", type=dict, help="Attributes dict")
    attr_parser.set_defaults(func=set_file_attributes_cmd)

    # Folder operations
    folder_parser = subparsers.add_parser("folder", help="Folder operations")
    folder_subparsers = folder_parser.add_subparsers(
        dest="subcommand", help="Folder subcommands"
    )

    # Folder create
    folder_create_parser = folder_subparsers.add_parser(
        "create", help="Create a new folder"
    )
    folder_create_parser.add_argument("path", help="Folder path")
    folder_create_parser.add_argument(
        "--parents", action="store_true", help="Create parent directories"
    )
    folder_create_parser.set_defaults(func=create_folder_cmd)

    # Folder delete
    folder_delete_parser = folder_subparsers.add_parser(
        "delete", help="Delete a folder"
    )
    folder_delete_parser.add_argument("path", help="Folder path")
    folder_delete_parser.add_argument(
        "--recursive", action="store_true", help="Delete recursively"
    )
    folder_delete_parser.add_argument(
        "--force", action="store_true", help="Force deletion"
    )
    folder_delete_parser.set_defaults(func=delete_folder_cmd)

    # Folder list
    folder_list_parser = folder_subparsers.add_parser(
        "list", help="List folder contents"
    )
    folder_list_parser.add_argument("path", help="Folder path")
    folder_list_parser.add_argument(
        "--recursive", action="store_true", help="List recursively"
    )
    folder_list_parser.add_argument(
        "--include-hidden", action="store_true", help="Include hidden files"
    )
    folder_list_parser.add_argument("--filter", help="File filter pattern")
    folder_list_parser.set_defaults(func=list_folder_cmd)

    # Folder copy
    folder_copy_parser = folder_subparsers.add_parser("copy", help="Copy a folder")
    folder_copy_parser.add_argument("source", help="Source path")
    folder_copy_parser.add_argument("destination", help="Destination path")
    folder_copy_parser.add_argument(
        "--recursive", action="store_true", help="Copy recursively"
    )
    folder_copy_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite destination"
    )
    folder_copy_parser.set_defaults(func=copy_folder_cmd)

    # Folder move
    folder_move_parser = folder_subparsers.add_parser("move", help="Move a folder")
    folder_move_parser.add_argument("source", help="Source path")
    folder_move_parser.add_argument("destination", help="Destination path")
    folder_move_parser.add_argument(
        "--overwrite", action="store_true", help="Overwrite destination"
    )
    folder_move_parser.set_defaults(func=move_folder_cmd)

    # Folder info
    folder_info_parser = folder_subparsers.add_parser(
        "info", help="Get folder information"
    )
    folder_info_parser.add_argument("path", help="Folder path")
    folder_info_parser.set_defaults(func=get_folder_info_cmd)

    # Folder rename
    folder_rename_parser = folder_subparsers.add_parser(
        "rename", help="Rename a folder"
    )
    folder_rename_parser.add_argument("path", help="Folder path")
    folder_rename_parser.add_argument("new_name", help="New name")
    folder_rename_parser.set_defaults(func=rename_folder_cmd)

    # Folder compress
    folder_compress_parser = folder_subparsers.add_parser(
        "compress", help="Compress a folder"
    )
    folder_compress_parser.add_argument("path", help="Folder path")
    folder_compress_parser.add_argument("archive_path", help="Archive path")
    folder_compress_parser.add_argument(
        "--format", choices=["zip", "tar", "gz"], default="zip", help="Archive format"
    )
    folder_compress_parser.set_defaults(func=compress_folder_cmd)

    # Folder size
    folder_size_parser = folder_subparsers.add_parser("size", help="Get folder size")
    folder_size_parser.add_argument("path", help="Folder path")
    folder_size_parser.set_defaults(func=get_folder_size_cmd)

    # Folder duplicates
    folder_duplicates_parser = folder_subparsers.add_parser(
        "duplicates", help="Find duplicate files"
    )
    folder_duplicates_parser.add_argument("path", help="Folder path")
    folder_duplicates_parser.add_argument(
        "--recursive", action="store_true", help="Search recursively"
    )
    folder_duplicates_parser.set_defaults(func=find_duplicates_cmd)

    # System operations
    system_parser = subparsers.add_parser("system", help="System operations")
    system_subparsers = system_parser.add_subparsers(
        dest="subcommand", help="System subcommands"
    )

    # System cwd
    cwd_parser = system_subparsers.add_parser(
        "cwd", help="Get current working directory"
    )
    cwd_parser.set_defaults(func=get_cwd_cmd)

    # System cd
    cd_parser = system_subparsers.add_parser("cd", help="Change directory")
    cd_parser.add_argument("path", help="Directory path")
    cd_parser.set_defaults(func=change_directory_cmd)

    # System exists
    exists_parser = system_subparsers.add_parser("exists", help="Check if path exists")
    exists_parser.add_argument("path", help="Path to check")
    exists_parser.set_defaults(func=path_exists_cmd)

    # System type
    type_parser = system_subparsers.add_parser("type", help="Get path type")
    type_parser.add_argument("path", help="Path to check")
    type_parser.set_defaults(func=get_path_type_cmd)

    # System disk
    disk_parser = system_subparsers.add_parser("disk", help="Get disk usage")
    disk_parser.add_argument("--path", help="Path to check")
    disk_parser.set_defaults(func=get_disk_usage_cmd)

    # System bookmark create
    bookmark_create_parser = system_subparsers.add_parser(
        "bookmark-create", help="Create bookmark"
    )
    bookmark_create_parser.add_argument("path", help="Path to bookmark")
    bookmark_create_parser.add_argument("name", help="Bookmark name")
    bookmark_create_parser.set_defaults(func=create_bookmark_cmd)

    # System bookmark list
    bookmark_list_parser = system_subparsers.add_parser(
        "bookmark-list", help="List bookmarks"
    )
    bookmark_list_parser.set_defaults(func=list_bookmarks_cmd)

    # System batch rename
    batch_parser = system_subparsers.add_parser(
        "batch-rename", help="Batch rename files"
    )
    batch_parser.add_argument("paths", nargs="+", help="File paths")
    batch_parser.add_argument("pattern", help="Rename pattern")
    batch_parser.set_defaults(func=batch_rename_cmd)

    # Advanced operations
    advanced_parser = subparsers.add_parser("advanced", help="Advanced operations")
    advanced_subparsers = advanced_parser.add_subparsers(
        dest="subcommand", help="Advanced subcommands"
    )

    # Advanced search
    search_parser = advanced_subparsers.add_parser("search", help="Search for files")
    search_parser.add_argument("path", help="Directory to search")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument(
        "--recursive", action="store_true", help="Search recursively"
    )
    search_parser.add_argument(
        "--case-sensitive", action="store_true", help="Case sensitive search"
    )
    search_parser.set_defaults(func=search_files_cmd)

    # Advanced index
    index_parser = advanced_subparsers.add_parser("index", help="Index files")
    index_parser.add_argument("path", help="Directory to index")
    index_parser.add_argument("--index-path", help="Index file path")
    index_parser.set_defaults(func=index_files_cmd)

    # Advanced permissions set
    perm_set_parser = advanced_subparsers.add_parser("perm-set", help="Set permissions")
    perm_set_parser.add_argument("path", help="Path")
    perm_set_parser.add_argument("permissions", help="Permissions string")
    perm_set_parser.set_defaults(func=set_permissions_cmd)

    # Advanced permissions get
    perm_get_parser = advanced_subparsers.add_parser("perm-get", help="Get permissions")
    perm_get_parser.add_argument("path", help="Path")
    perm_get_parser.set_defaults(func=get_permissions_cmd)

    # Advanced encrypt
    encrypt_parser = advanced_subparsers.add_parser("encrypt", help="Encrypt file")
    encrypt_parser.add_argument("path", help="File path")
    encrypt_parser.add_argument("password", help="Encryption password")
    encrypt_parser.set_defaults(func=encrypt_file_cmd)

    # Advanced decrypt
    decrypt_parser = advanced_subparsers.add_parser("decrypt", help="Decrypt file")
    decrypt_parser.add_argument("path", help="File path")
    decrypt_parser.add_argument("password", help="Decryption password")
    decrypt_parser.set_defaults(func=decrypt_file_cmd)

    # Development operations
    dev_parser = subparsers.add_parser("dev", help="Development tools")
    dev_subparsers = dev_parser.add_subparsers(
        dest="subcommand", help="Development subcommands"
    )

    # Dev format
    format_parser = dev_subparsers.add_parser("format", help="Format code with black")
    format_parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to format (default: current directory)",
    )
    format_parser.set_defaults(func=format_code_cmd)

    # Dev lint
    lint_parser = dev_subparsers.add_parser("lint", help="Lint code with flake8")
    lint_parser.add_argument(
        "path", nargs="?", default=".", help="Path to lint (default: current directory)"
    )
    lint_parser.set_defaults(func=lint_code_cmd)

    return parser
