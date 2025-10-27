import pytest
from cli.utils import print_success, print_error, print_warning, print_info, Colors
import io
import sys


class TestColors:
    def test_colors_defined(self):
        assert Colors.GREEN == "\033[92m"
        assert Colors.RED == "\033[91m"
        assert Colors.YELLOW == "\033[93m"
        assert Colors.BLUE == "\033[94m"
        assert Colors.RESET == "\033[0m"


class TestPrintFunctions:
    def test_print_success(self, capsys):
        print_success("Test message")
        captured = capsys.readouterr()
        assert Colors.GREEN in captured.out
        assert "✓" in captured.out
        assert "Test message" in captured.out
        assert Colors.RESET in captured.out

    def test_print_error(self, capsys):
        print_error("Test error")
        captured = capsys.readouterr()
        assert Colors.RED in captured.out
        assert "✗" in captured.out
        assert "Test error" in captured.out

    def test_print_warning(self, capsys):
        print_warning("Test warning")
        captured = capsys.readouterr()
        assert Colors.YELLOW in captured.out
        assert "!" in captured.out
        assert "Test warning" in captured.out

    def test_print_info(self, capsys):
        print_info("Test info")
        captured = capsys.readouterr()
        assert Colors.BLUE in captured.out
        assert "ℹ" in captured.out
        assert "Test info" in captured.out
