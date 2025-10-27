import os


def search_files(path, query, recursive=True, case_sensitive=False):
    """
    Searches for files matching criteria.

    Parameters:
    - path (str): The directory to search in.
    - query (str): Search query (name, content, etc.).
    - recursive (bool, optional): Whether to search recursively. Defaults to True.
    - case_sensitive (bool, optional): Case sensitivity. Defaults to False.

    Returns:
    List of matching file paths on success, or error message on failure.

    Errors:
    - Path not found
    - permission denied
    """
    try:
        matches = []
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                if case_sensitive:
                    if query in file:
                        matches.append(file_path)
                else:
                    if query.lower() in file.lower():
                        matches.append(file_path)
            if not recursive:
                break
        return matches
    except FileNotFoundError:
        return "Path not found"
    except PermissionError:
        return "permission denied"


def index_files(path, index_path=None):
    """
    Creates an index of files for faster searching.

    Parameters:
    - path (str): The directory to index.
    - index_path (str, optional): Path to save the index. Defaults to default location.

    Returns:
    Success status (bool) and index path on success, or error message on failure.

    Errors:
    - Path not found
    - permission denied
    """
    try:
        index = {}
        for root, dirs, files in os.walk(path):
            for file in files:
                file_path = os.path.join(root, file)
                index[file] = file_path
        if index_path is None:
            index_path = os.path.join(path, "index.json")
        import json

        with open(index_path, "w") as f:
            json.dump(index, f)
        return True, index_path
    except FileNotFoundError:
        return False, "Path not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def set_permissions(path, permissions):
    """
    Sets file/folder permissions.

    Parameters:
    - path (str): The full path to the file/folder.
    - permissions (str): Permission string (e.g., '755' for Unix).

    Returns:
    Success status (bool) on success, or error message on failure.

    Errors:
    - Path not found
    - permission denied
    """
    try:
        os.chmod(path, int(permissions, 8))
        return True
    except FileNotFoundError:
        return False, "Path not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def get_permissions(path):
    """
    Gets file/folder permissions.

    Parameters:
    - path (str): The full path to the file/folder.

    Returns:
    Permission string on success, or error message on failure.

    Errors:
    - Path not found
    - permission denied
    """
    try:
        st = os.stat(path)
        return oct(st.st_mode)[-3:]
    except FileNotFoundError:
        return "Path not found"
    except PermissionError:
        return "permission denied"


def encrypt_file(path, password):
    """
    Encrypts a file.

    Parameters:
    - path (str): The full path to the file.
    - password (str): Encryption password.

    Returns:
    Success status (bool) and encrypted file path on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    """
    # Simple XOR encryption for demo, not secure
    try:
        with open(path, "rb") as f:
            data = f.read()
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ ord(password[i % len(password)]))
        enc_path = path + ".enc"
        with open(enc_path, "wb") as f:
            f.write(encrypted)
        return True, enc_path
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, str(e)


def decrypt_file(path, password):
    """
    Decrypts a file.

    Parameters:
    - path (str): The full path to the encrypted file.
    - password (str): Decryption password.

    Returns:
    Success status (bool) and decrypted file path on success, or error message on failure.

    Errors:
    - File not found
    - permission denied
    - wrong password
    """
    try:
        with open(path, "rb") as f:
            data = f.read()
        decrypted = bytearray()
        for i, byte in enumerate(data):
            decrypted.append(byte ^ ord(password[i % len(password)]))
        dec_path = path.replace(".enc", "")
        with open(dec_path, "wb") as f:
            f.write(decrypted)
        return True, dec_path
    except FileNotFoundError:
        return False, "File not found"
    except PermissionError:
        return False, "permission denied"
    except Exception as e:
        return False, "wrong password"
