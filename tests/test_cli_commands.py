import pytest
import tempfile
import os
import subprocess
import sys
from cli.main import main
from cli.parsers import setup_parsers


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


class TestCLICommands:
    def test_file_create_command(self, temp_dir, capsys):
        path = os.path.join(temp_dir, "new.txt")
        # Simulate command line args
        original_argv = sys.argv
        sys.argv = ["faf", "file", "create", path, "--content", "test content"]
        try:
            main()
            captured = capsys.readouterr()
            assert "File created" in captured.out
            assert os.path.exists(path)
        finally:
            sys.argv = original_argv

    def test_file_read_command(self, temp_file, capsys):
        original_argv = sys.argv
        sys.argv = ["faf", "file", "read", temp_file]
        try:
            main()
            captured = capsys.readouterr()
            assert "Contents of" in captured.out
            assert "Hello World" in captured.out
        finally:
            sys.argv = original_argv

    def test_file_delete_command(self, temp_file, capsys):
        original_argv = sys.argv
        sys.argv = ["faf", "file", "delete", temp_file, "--force"]
        try:
            main()
            captured = capsys.readouterr()
            assert "File deleted" in captured.out
            assert not os.path.exists(temp_file)
        finally:
            sys.argv = original_argv

    def test_folder_create_command(self, temp_dir, capsys):
        path = os.path.join(temp_dir, "new_folder")
        original_argv = sys.argv
        sys.argv = ["faf", "folder", "create", path]
        try:
            main()
            captured = capsys.readouterr()
            assert "Folder created" in captured.out or "created" in captured.out.lower()
            assert os.path.exists(path)
        finally:
            sys.argv = original_argv

    def test_folder_list_command(self, temp_dir, capsys):
        # Create a file in temp_dir
        with open(os.path.join(temp_dir, "file.txt"), "w") as f:
            f.write("test")
        original_argv = sys.argv
        sys.argv = ["faf", "folder", "list", temp_dir]
        try:
            main()
            captured = capsys.readouterr()
            assert "file.txt" in captured.out
        finally:
            sys.argv = original_argv

    def test_system_cwd_command(self, capsys):
        original_argv = sys.argv
        sys.argv = ["faf", "system", "cwd"]
        try:
            main()
            captured = capsys.readouterr()
            assert os.getcwd() in captured.out
        finally:
            sys.argv = original_argv

    def test_invalid_command(self, capsys):
        original_argv = sys.argv
        sys.argv = ["faf", "invalid"]
        try:
            with pytest.raises(SystemExit):
                main()
            captured = capsys.readouterr()
            assert "invalid choice" in captured.err
        finally:
            sys.argv = original_argv
