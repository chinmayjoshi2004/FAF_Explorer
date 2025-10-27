import pytest
import tempfile
import os
from core.folder_system_operation import (
    create_folder,
    delete_folder,
    list_folder,
    copy_folder,
    move_folder,
    get_folder_info,
    rename_folder,
    compress_folder,
    get_folder_size,
    find_duplicates,
)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_folder(temp_dir):
    folder_path = os.path.join(temp_dir, "test_folder")
    os.makedirs(folder_path)
    return folder_path


class TestCreateFolder:
    def test_create_folder_success(self, temp_dir):
        path = os.path.join(temp_dir, "new_folder")
        success, result = create_folder(path)
        assert success is True
        assert result == path
        assert os.path.exists(path)

    def test_create_folder_exists(self, temp_folder):
        success, result = create_folder(temp_folder)
        assert success is False
        assert result == "Folder already exists"

    def test_create_folder_with_parents(self, temp_dir):
        path = os.path.join(temp_dir, "parent", "child")
        success, result = create_folder(path, parents=True)
        assert success is True
        assert os.path.exists(path)


class TestDeleteFolder:
    def test_delete_folder_success(self, temp_folder):
        success = delete_folder(temp_folder)
        assert success is True
        assert not os.path.exists(temp_folder)

    def test_delete_folder_not_empty(self, temp_folder):
        # Add a file
        with open(os.path.join(temp_folder, "file.txt"), "w") as f:
            f.write("test")
        result = delete_folder(temp_folder)
        assert result == (False, "folder not empty")

    def test_delete_folder_recursive(self, temp_folder):
        with open(os.path.join(temp_folder, "file.txt"), "w") as f:
            f.write("test")
        success = delete_folder(temp_folder, recursive=True)
        assert success is True
        assert not os.path.exists(temp_folder)


class TestListFolder:
    def test_list_folder_success(self, temp_folder):
        # Create some files
        with open(os.path.join(temp_folder, "file1.txt"), "w") as f:
            f.write("test1")
        with open(os.path.join(temp_folder, "file2.txt"), "w") as f:
            f.write("test2")
        items = list_folder(temp_folder)
        assert len(items) == 2
        assert "file1.txt" in items
        assert "file2.txt" in items

    def test_list_folder_recursive(self, temp_folder):
        subfolder = os.path.join(temp_folder, "sub")
        os.makedirs(subfolder)
        with open(os.path.join(subfolder, "file.txt"), "w") as f:
            f.write("test")
        items = list_folder(temp_folder, recursive=True)
        assert len(items) == 2  # sub and file.txt


class TestCopyFolder:
    def test_copy_folder_success(self, temp_folder, temp_dir):
        dest = os.path.join(temp_dir, "copy_folder")
        success, result = copy_folder(temp_folder, dest)
        assert success is True
        assert result == dest
        assert os.path.exists(dest)


class TestMoveFolder:
    def test_move_folder_success(self, temp_folder, temp_dir):
        dest = os.path.join(temp_dir, "moved_folder")
        success, result = move_folder(temp_folder, dest)
        assert success is True
        assert result == dest
        assert not os.path.exists(temp_folder)
        assert os.path.exists(dest)


class TestGetFolderInfo:
    def test_get_folder_info_success(self, temp_folder):
        info = get_folder_info(temp_folder)
        assert isinstance(info, dict)
        assert "size" in info
        assert "item_count" in info


class TestRenameFolder:
    def test_rename_folder_success(self, temp_folder):
        new_path = temp_folder.replace("test_folder", "renamed_folder")
        success, result = rename_folder(temp_folder, "renamed_folder")
        assert success is True
        assert result == new_path
        assert not os.path.exists(temp_folder)
        assert os.path.exists(new_path)


class TestCompressFolder:
    def test_compress_folder_zip(self, temp_folder, temp_dir):
        archive = os.path.join(temp_dir, "folder_archive.zip")
        success, result = compress_folder(temp_folder, archive, "zip")
        assert success is True
        assert os.path.exists(archive)


class TestGetFolderSize:
    def test_get_folder_size_success(self, temp_folder):
        with open(os.path.join(temp_folder, "file.txt"), "w") as f:
            f.write("test content")
        size = get_folder_size(temp_folder)
        assert isinstance(size, int)
        assert size > 0


class TestFindDuplicates:
    def test_find_duplicates_none(self, temp_folder):
        with open(os.path.join(temp_folder, "file1.txt"), "w") as f:
            f.write("unique")
        with open(os.path.join(temp_folder, "file2.txt"), "w") as f:
            f.write("different")
        duplicates = find_duplicates(temp_folder)
        assert duplicates == []

    def test_find_duplicates_found(self, temp_folder):
        content = "duplicate content"
        with open(os.path.join(temp_folder, "file1.txt"), "w") as f:
            f.write(content)
        with open(os.path.join(temp_folder, "file2.txt"), "w") as f:
            f.write(content)
        duplicates = find_duplicates(temp_folder)
        assert len(duplicates) == 1
        assert len(duplicates[0]) == 2
