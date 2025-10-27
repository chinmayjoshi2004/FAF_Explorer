import os
import shutil
import hashlib
import filecmp
import zipfile
import tarfile


def create_file(path, content="", overwrite=False):
    """
    Creates a new file at the specified path with optional initial content.

    Parameters:
    - path (str): The full path where the file should be created, including filename and extension.
    - content (str, optional): Initial content to write to the file. Defaults to empty string.
    - overwrite (bool, optional): Whether to overwrite the file if it already exists. Defaults to False.

    Returns:
    Success status (bool) and file path on success, or error message on failure.

    Errors:
    - File already exists (if overwrite=False)
    - permission denied
    - invalid path
    """
    try:
        if os.path.exists(path) and not overwrite:
            return False, "File already exists"
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return True, path
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, f"invalid path: {str(e)}"


def read_file(path, encoding=None):
    """
    Reads the contents of an existing file.

    Parameters:
    - path (str): The full path to the file to read.
    - encoding (str, optional): Character encoding (e.g., 'utf-8'). Defaults to system default.

    Returns:
    File contents as string on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - invalid path
    """
    try:
        with open(path, "r", encoding=encoding) as f:
            return f.read()
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "permission denied"
    except Exception as e:
        return f"invalid path: {str(e)}"


def write_file(path, content, mode="w", encoding=None):
    """
    Writes content to an existing file, optionally appending or overwriting.

    Parameters:
    - path (str): The full path to the file to write to.
    - content (str): Content to write to the file.
    - mode (str, optional): Write mode ('w' for overwrite, 'a' for append). Defaults to 'w'.
    - encoding (str, optional): Character encoding. Defaults to system default.

    Returns:
    Success status (bool) and bytes written on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - invalid path
    """
    try:
        with open(path, mode, encoding=encoding) as f:
            bytes_written = f.write(content)
        return True, bytes_written
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, f"invalid path: {str(e)}"


def delete_file(path, force=False):
    """
    Deletes an existing file.

    Parameters:
    - path (str): The full path to the file to delete.
    - force (bool, optional): Whether to force deletion even if file is read-only. Defaults to False.

    Returns:
    Success status (bool) on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - file in use
    """
    try:
        if force:
            os.chmod(path, 0o777)  # Make writable
        os.remove(path)
        return True
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except OSError as e:
        return False, f"file in use: {str(e)}"


def copy_file(source_path, destination_path, overwrite=False):
    """
    Copies a file from source to destination.

    Parameters:
    - source_path (str): The full path to the source file.
    - destination_path (str): The full path to the destination file.
    - overwrite (bool, optional): Whether to overwrite destination if it exists. Defaults to False.

    Returns:
    Success status (bool) and destination path on success, or error message on failure.

    Errors:
    - Source file not found
    - destination exists (if overwrite=False)
    - permission denied
    """
    try:
        if os.path.exists(destination_path) and not overwrite:
            return False, "destination exists"
        shutil.copy2(source_path, destination_path)
        return True, destination_path
    except FileNotFoundError:
        return False, "Source file not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def move_file(source_path, destination_path, overwrite=False):
    """
    Moves a file from source to destination (equivalent to rename if same directory).

    Parameters:
    - source_path (str): The full path to the source file.
    - destination_path (str): The full path to the destination file.
    - overwrite (bool, optional): Whether to overwrite destination if it exists. Defaults to False.

    Returns:
    Success status (bool) and new path on success, or error message on failure.

    Errors:
    - Source file not found
    - destination exists (if overwrite=False)
    - permission denied
    """
    try:
        if os.path.exists(destination_path) and not overwrite:
            return False, "destination exists"
        shutil.move(source_path, destination_path)
        return True, destination_path
    except FileNotFoundError:
        return False, "Source file not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def get_file_info(path):
    """
    Retrieves metadata about a file.

    Parameters:
    - path (str): The full path to the file.

    Returns:
    Dictionary/object containing size, creation date, modification date, permissions, etc., or error message on failure.

    Errors:
    - File not found
    - permission denied
    """
    try:
        stat = os.stat(path)
        return {
            "size": stat.st_size,
            "creation_date": stat.st_ctime,
            "modification_date": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:],
        }
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "permission denied"


def rename_file(path, new_name):
    """
    Renames a file.

    Parameters:
    - path (str): The full path to the file to rename.
    - new_name (str): The new name for the file.

    Returns:
    Success status (bool) and new path on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - name conflict
    """
    try:
        dir_path = os.path.dirname(path)
        new_path = os.path.join(dir_path, new_name)
        if os.path.exists(new_path):
            return False, "name conflict"
        os.rename(path, new_path)
        return True, new_path
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def compress_file(path, archive_path, format="zip"):
    """
    Compresses a file into an archive.

    Parameters:
    - path (str): The full path to the file to compress.
    - archive_path (str): The path for the output archive.
    - format (str, optional): Archive format (zip, tar, gz). Defaults to zip.

    Returns:
    Success status (bool) and archive path on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - invalid format
    """
    try:
        if format == "zip":
            with zipfile.ZipFile(archive_path, "w") as zf:
                zf.write(path, os.path.basename(path))
        elif format in ["tar", "gz"]:
            with tarfile.open(archive_path, f"w:{format}") as tf:
                tf.add(path, arcname=os.path.basename(path))
        else:
            return False, "invalid format"
        return True, archive_path
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def decompress_file(archive_path, destination):
    """
    Decompresses an archive.

    Parameters:
    - archive_path (str): The full path to the archive.
    - destination (str): The destination directory.

    Returns:
    Success status (bool) and extracted files list on success, or error message on failure.

    Errors:
    - Archive not found
    - permission denied
    - corrupted archive
    """
    try:
        if zipfile.is_zipfile(archive_path):
            with zipfile.ZipFile(archive_path, "r") as zf:
                zf.extractall(destination)
                return True, zf.namelist()
        elif tarfile.is_tarfile(archive_path):
            with tarfile.open(archive_path, "r") as tf:
                tf.extractall(destination)
                return True, tf.getnames()
        else:
            return False, "corrupted archive"
    except FileNotFoundError:
        return False, "Archive not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, f"corrupted archive: {str(e)}"


def create_symlink(target_path, link_path):
    """
    Creates a symbolic link to a file.

    Parameters:
    - target_path (str): The path to the target file.
    - link_path (str): The path for the symbolic link.

    Returns:
    Success status (bool) and link path on success, or error message on failure.

    Errors:
    - Target not found
    - permission denied
    - link exists
    """
    try:
        if os.path.exists(link_path):
            return False, "link exists"
        os.symlink(target_path, link_path)
        return True, link_path
    except FileNotFoundError:
        return False, "Target not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def get_file_hash(path, algorithm="sha256"):
    """
    Calculates hash (MD5, SHA256) of a file.

    Parameters:
    - path (str): The full path to the file.
    - algorithm (str, optional): Hash algorithm. Defaults to SHA256.

    Returns:
    Hash string on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    """
    try:
        hash_func = hashlib.new(algorithm.lower())
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "permission denied"
    except Exception as e:
        return str(e)


def compare_files(path1, path2):
    """
    Compares two files for differences.

    Parameters:
    - path1 (str): Path to first file.
    - path2 (str): Path to second file.

    Returns:
    Comparison result (differences or identical) on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    """
    try:
        if filecmp.cmp(path1, path2, shallow=False):
            return "identical"
        else:
            return "differences"
    except FileNotFoundError:
        return "File not found"
    except PermissionError:
        return "permission denied"
    except Exception as e:
        return str(e)


def set_file_attributes(path, attributes):
    """
    Sets file attributes (hidden, read-only).

    Parameters:
    - path (str): The full path to the file.
    - attributes (dict): Attributes to set (e.g., {'hidden': true, 'readonly': false}).

    Returns:
    Success status (bool) on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    """
    try:
        current_mode = os.stat(path).st_mode
        if attributes.get("readonly", False):
            os.chmod(path, current_mode & ~0o222)  # Remove write permissions
        else:
            os.chmod(path, current_mode | 0o222)  # Add write permissions
        # For hidden on Windows, would need win32api, but skip for now
        return True
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)
