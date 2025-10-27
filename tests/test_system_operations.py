import pytest
import tempfile
import os
from core.system_operation import (
    get_cwd,
    change_directory,
    path_exists,
    get_path_type,
    get_disk_usage,
    create_bookmark,
    list_bookmarks,
    batch_rename,
)


@pytest.fixture
def temp_dir():
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_file(temp_dir):
    file_path = os.path.join(temp_dir, "test.txt")
    with open(file_path, "w") as f:
        f.write("Hello World")
    return file_path


class TestGetCwd:
    def test_get_cwd(self):
        cwd = get_cwd()
        assert isinstance(cwd, str)
        assert os.path.exists(cwd)


class TestChangeDirectory:
    def test_change_directory_success(self, temp_dir):
        original_cwd = get_cwd()
        success, new_cwd = change_directory(temp_dir)
        assert success is True
        assert new_cwd == temp_dir
        # Change back
        change_directory(original_cwd)

    def test_change_directory_not_found(self):
        success, result = change_directory("/nonexistent/path")
        assert success is False
        assert result == "Directory not found"


class TestPathExists:
    def test_path_exists_file(self, temp_file):
        assert path_exists(temp_file) is True

    def test_path_exists_folder(self, temp_dir):
        assert path_exists(temp_dir) is True

    def test_path_exists_false(self):
        assert path_exists("/nonexistent/path") is False


class TestGetPathType:
    def test_get_path_type_file(self, temp_file):
        result = get_path_type(temp_file)
        assert result == "file"

    def test_get_path_type_folder(self, temp_dir):
        result = get_path_type(temp_dir)
        assert result == "folder"

    def test_get_path_type_unknown(self, temp_dir):
        # Test nonexistent path - os.path.isfile/isdir return False for nonexistent, so 'unknown'
        result = get_path_type(os.path.join(temp_dir, "nonexistent"))
        assert result == "unknown"


class TestGetDiskUsage:
    def test_get_disk_usage(self, temp_dir):
        usage = get_disk_usage(temp_dir)
        assert isinstance(usage, dict)
        assert "total" in usage
        assert "used" in usage
        assert "free" in usage


class TestCreateBookmark:
    def test_create_bookmark_success(self, temp_dir):
        success = create_bookmark(temp_dir, "test_bookmark")
        assert success is True

    def test_create_bookmark_not_found(self):
        success, result = create_bookmark("/nonexistent", "test")
        assert success is False
        assert result == "Path not found"


class TestListBookmarks:
    def test_list_bookmarks(self):
        bookmarks = list_bookmarks()
        assert isinstance(bookmarks, list)


class TestBatchRename:
    def test_batch_rename_success(self, temp_dir):
        file1 = os.path.join(temp_dir, "file1.txt")
        file2 = os.path.join(temp_dir, "file2.txt")
        with open(file1, "w") as f:
            f.write("test1")
        with open(file2, "w") as f:
            f.write("test2")
        success, renamed = batch_rename([file1, file2], "new_{old}")
        assert success is True
        assert len(renamed) == 2
        assert "new_file1.txt" in [os.path.basename(p) for p in renamed]
        assert "new_file2.txt" in [os.path.basename(p) for p in renamed]
