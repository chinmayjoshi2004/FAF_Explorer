import os
import shutil


def create_folder(path, parents=False):
    """
    Creates a new directory at the specified path.

    Parameters:
    - path (str): The full path where the folder should be created.
    - parents (bool, optional): Whether to create parent directories if they don't exist. Defaults to False.

    Returns:
    Success status (bool) and folder path on success, or error message on failure.

    Errors:
    - Folder already exists
    - permission denied
    - invalid path
    """
    try:
        if parents:
            os.makedirs(path, exist_ok=True)
        else:
            os.mkdir(path)
        return True, path
    except FileExistsError:
        return False, "Folder already exists"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, f"invalid path: {str(e)}"


def delete_folder(path, recursive=False, force=False):
    """
    Deletes an existing directory.

    Parameters:
    - path (str): The full path to the folder to delete.
    - recursive (bool, optional): Whether to delete recursively (including contents). Defaults to False.
    - force (bool, optional): Whether to force deletion even if read-only. Defaults to False.

    Returns:
    Success status (bool) and None on success, or False and error message on failure.

    Errors:
    - Folder not found
    - folder not empty (if recursive=False)
    - permission denied
    """
    try:
        if recursive:
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        return True, None
    except FileNotFoundError:
        return False, "Folder not found"
    except OSError as e:
        if "not empty" in str(e).lower():
            return False, "folder not empty"
        return False, str(e)
    except PermissionError:
        return False, "permission denied"


def list_folder(path, recursive=False, include_hidden=False, filter=None):
    """
    Lists the contents of a directory.

    Parameters:
    - path (str): The full path to the folder to list.
    - recursive (bool, optional): Whether to list recursively. Defaults to False.
    - include_hidden (bool, optional): Whether to include hidden files/folders. Defaults to False.
    - filter (str, optional): File extension or pattern to filter results (e.g., '*.txt').

    Returns:
    List of file/folder names or full paths on success, or error message on failure.

    Errors:
    - Folder not found
    - permission denied
    """
    try:
        items = []
        for root, dirs, files in os.walk(path):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                files = [f for f in files if not f.startswith(".")]
            for item in dirs + files:
                full_path = os.path.join(root, item)
                if filter:
                    import fnmatch

                    if not fnmatch.fnmatch(full_path, filter):
                        continue
                if recursive:
                    items.append(full_path)
                else:
                    items.append(item)
            if not recursive:
                break
        return items
    except FileNotFoundError:
        return "Folder not found"
    except PermissionError:
        return "permission denied"


def copy_folder(source_path, destination_path, recursive=True, overwrite=False):
    """
    Copies a folder and its contents from source to destination.

    Parameters:
    - source_path (str): The full path to the source folder.
    - destination_path (str): The full path to the destination folder.
    - recursive (bool, optional): Whether to copy recursively. Defaults to True.
    - overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.

    Returns:
    Success status (bool) and destination path on success, or error message on failure.

    Errors:
    - Source folder not found
    - destination exists
    - permission denied
    """
    try:
        if os.path.exists(destination_path) and not overwrite:
            return False, "destination exists"
        shutil.copytree(source_path, destination_path, dirs_exist_ok=overwrite)
        return True, destination_path
    except FileNotFoundError:
        return False, "Source folder not found"
    except FileExistsError:
        return False, "destination exists"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def move_folder(source_path, destination_path, overwrite=False):
    """
    Moves a folder and its contents from source to destination.

    Parameters:
    - source_path (str): The full path to the source folder.
    - destination_path (str): The full path to the destination folder.
    - overwrite (bool, optional): Whether to overwrite existing files. Defaults to False.

    Returns:
    Success status (bool) and new path on success, or error message on failure.

    Errors:
    - Source folder not found
    - destination exists
    - permission denied
    """
    try:
        if os.path.exists(destination_path) and not overwrite:
            return False, "destination exists"
        shutil.move(source_path, destination_path)
        return True, destination_path
    except FileNotFoundError:
        return False, "Source folder not found"
    except FileExistsError:
        return False, "destination exists"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def get_folder_info(path):
    """
    Retrieves metadata about a folder.

    Parameters:
    - path (str): The full path to the folder.

    Returns:
    Dictionary/object containing size, creation date, modification date, permissions, item count, etc., or error message on failure.

    Errors:
    - Folder not found
    - permission denied
    """
    try:
        stat = os.stat(path)
        item_count = len(os.listdir(path))
        return {
            "size": stat.st_size,
            "creation_date": stat.st_ctime,
            "modification_date": stat.st_mtime,
            "permissions": oct(stat.st_mode)[-3:],
            "item_count": item_count,
        }
    except FileNotFoundError:
        return "Folder not found"
    except PermissionError:
        return "permission denied"


def rename_folder(path, new_name):
    """
    Renames a folder.

    Parameters:
    - path (str): The full path to the folder to rename.
    - new_name (str): The new name for the folder.

    Returns:
    Success status (bool) and new path on success, or error message on failure.

    Errors:
    - Folder not found
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
        return False, "Folder not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def compress_folder(path, archive_path, format="zip"):
    """
    Compresses a folder into an archive.

    Parameters:
    - path (str): The full path to the folder to compress.
    - archive_path (str): The path for the output archive.
    - format (str, optional): Archive format. Defaults to zip.

    Returns:
    Success status (bool) and archive path on success, or error message on failure.

    Errors:
    - Folder not found
    - permission denied
    - invalid format
    """
    try:
        if format == "zip":
            shutil.make_archive(archive_path.replace(".zip", ""), "zip", path)
        elif format in ["tar", "gz"]:
            shutil.make_archive(archive_path.replace(f".{format}", ""), format, path)
        else:
            return False, "invalid format"
        return True, archive_path
    except FileNotFoundError:
        return False, "Folder not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def get_folder_size(path):
    """
    Calculates the total size of a folder.

    Parameters:
    - path (str): The full path to the folder.

    Returns:
    Total size in bytes on success, or error message on failure.

    Errors:
    - Folder not found
    - permission denied
    """
    try:
        total_size = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                total_size += os.path.getsize(os.path.join(root, file))
        return total_size
    except FileNotFoundError:
        return "Folder not found"
    except PermissionError:
        return "permission denied"


def find_duplicates(path, recursive=True):
    """
    Finds duplicate files in a folder.

    Parameters:
    - path (str): The full path to the folder to scan.
    - recursive (bool, optional): Whether to scan recursively. Defaults to True.

    Returns:
    List of duplicate file groups on success, or error message on failure.

    Errors:
    - Folder not found
    - permission denied
    """
    try:
        file_hashes = {}
        duplicates = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = get_file_hash(file_path)
                if file_hash in file_hashes:
                    file_hashes[file_hash].append(file_path)
                else:
                    file_hashes[file_hash] = [file_path]
            if not recursive:
                break
        for hash_val, paths in file_hashes.items():
            if len(paths) > 1:
                duplicates.append(paths)
        return duplicates
    except FileNotFoundError:
        return "Folder not found"
    except PermissionError:
        return "permission denied"


# Helper function for hash
def get_file_hash(path, algorithm="md5"):
    try:
        import hashlib

        hash_func = hashlib.new(algorithm.lower())
        with open(path, "rb") as f:
            while chunk := f.read(8192):
                hash_func.update(chunk)
        return hash_func.hexdigest()
    except:
        return None
