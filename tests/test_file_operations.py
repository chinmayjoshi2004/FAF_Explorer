import pytest
import tempfile
import os
from core.file_system_operation import (
    create_file,
    read_file,
    write_file,
    delete_file,
    copy_file,
    move_file,
    get_file_info,
    rename_file,
    compress_file,
    decompress_file,
    create_symlink,
    get_file_hash,
    compare_files,
    set_file_attributes,
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


class TestCreateFile:
    def test_create_file_success(self, temp_dir):
        path = os.path.join(temp_dir, "new.txt")
        success, result = create_file(path, "content")
        assert success is True
        assert result == path
        assert os.path.exists(path)

    def test_create_file_exists_no_overwrite(self, temp_file):
        success, result = create_file(temp_file, "new content")
        assert success is False
        assert result == "File already exists"

    def test_create_file_overwrite(self, temp_file):
        success, result = create_file(temp_file, "new content", overwrite=True)
        assert success is True
        assert result == temp_file
        with open(temp_file) as f:
            assert f.read() == "new content"


class TestReadFile:
    def test_read_file_success(self, temp_file):
        content = read_file(temp_file)
        assert content == "Hello World"

    def test_read_file_not_found(self, temp_dir):
        path = os.path.join(temp_dir, "nonexistent.txt")
        content = read_file(path)
        assert content == "File not found"


class TestWriteFile:
    def test_write_file_success(self, temp_file):
        success, bytes_written = write_file(temp_file, "New content")
        assert success is True
        assert bytes_written == len("New content")
        with open(temp_file) as f:
            assert f.read() == "New content"

    def test_write_file_append(self, temp_file):
        success, bytes_written = write_file(temp_file, " appended", mode="a")
        assert success is True
        assert bytes_written == len(" appended")
        with open(temp_file) as f:
            assert f.read() == "Hello World appended"


class TestDeleteFile:
    def test_delete_file_success(self, temp_file):
        success = delete_file(temp_file)
        assert success is True
        assert not os.path.exists(temp_file)

    def test_delete_file_not_found(self, temp_dir):
        path = os.path.join(temp_dir, "nonexistent.txt")
        result = delete_file(path)
        assert result == (False, "File not found")


class TestCopyFile:
    def test_copy_file_success(self, temp_file, temp_dir):
        dest = os.path.join(temp_dir, "copy.txt")
        success, result = copy_file(temp_file, dest)
        assert success is True
        assert result == dest
        assert os.path.exists(dest)

    def test_copy_file_dest_exists_no_overwrite(self, temp_file, temp_dir):
        dest = os.path.join(temp_dir, "copy.txt")
        copy_file(temp_file, dest)  # Create first
        success, result = copy_file(temp_file, dest)
        assert success is False
        assert result == "destination exists"


class TestMoveFile:
    def test_move_file_success(self, temp_file, temp_dir):
        dest = os.path.join(temp_dir, "moved.txt")
        success, result = move_file(temp_file, dest)
        assert success is True
        assert result == dest
        assert not os.path.exists(temp_file)
        assert os.path.exists(dest)


class TestGetFileInfo:
    def test_get_file_info_success(self, temp_file):
        info = get_file_info(temp_file)
        assert isinstance(info, dict)
        assert "size" in info
        assert "creation_date" in info

    def test_get_file_info_not_found(self, temp_dir):
        path = os.path.join(temp_dir, "nonexistent.txt")
        info = get_file_info(path)
        assert info == "File not found"


class TestRenameFile:
    def test_rename_file_success(self, temp_file):
        new_path = temp_file.replace("test.txt", "renamed.txt")
        success, result = rename_file(temp_file, "renamed.txt")
        assert success is True
        assert result == new_path
        assert not os.path.exists(temp_file)
        assert os.path.exists(new_path)


class TestCompressFile:
    def test_compress_file_zip(self, temp_file, temp_dir):
        archive = os.path.join(temp_dir, "archive.zip")
        success, result = compress_file(temp_file, archive, "zip")
        assert success is True
        assert result == archive
        assert os.path.exists(archive)


class TestDecompressFile:
    def test_decompress_file_zip(self, temp_file, temp_dir):
        archive = os.path.join(temp_dir, "archive.zip")
        compress_file(temp_file, archive, "zip")
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir)
        success, files = decompress_file(archive, extract_dir)
        assert success is True
        assert len(files) == 1


class TestGetFileHash:
    def test_get_file_hash_md5(self, temp_file):
        hash_val = get_file_hash(temp_file, "md5")
        assert isinstance(hash_val, str)
        assert len(hash_val) == 32


class TestCompareFiles:
    def test_compare_files_identical(self, temp_file, temp_dir):
        copy = os.path.join(temp_dir, "copy.txt")
        copy_file(temp_file, copy)
        result = compare_files(temp_file, copy)
        assert result == "identical"

    def test_compare_files_different(self, temp_file, temp_dir):
        other = os.path.join(temp_dir, "other.txt")
        create_file(other, "Different")
        result = compare_files(temp_file, other)
        assert result == "differences"


class TestSetFileAttributes:
    def test_set_file_attributes_readonly(self, temp_file):
        success = set_file_attributes(temp_file, {"readonly": True})
        assert success is True
