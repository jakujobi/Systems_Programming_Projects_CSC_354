import unittest
import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.ErrorLogHandler import ErrorLogHandler

class TestErrorLogHandler(unittest.TestCase):
    def setUp(self):
        self.error_handler = ErrorLogHandler()

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_basic_output(self, mock_stdout):
        self.error_handler.print_colored("Test Message", "red")
        self.assertIn("Test Message", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_with_custom_background(self, mock_stdout):
        self.error_handler.print_colored("Test Message", "white", "blue")
        self.assertIn("Test Message", mock_stdout.getvalue())

    def test_print_colored_invalid_color(self):
        with self.assertRaises(ValueError) as context:
            self.error_handler.print_colored("Test Message", "purple")
        self.assertIn("Unsupported color", str(context.exception))

    def test_print_colored_invalid_background(self):
        with self.assertRaises(ValueError) as context:
            self.error_handler.print_colored("Test Message", "red", "orange")
        self.assertIn("Unsupported background color", str(context.exception))

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_empty_string(self, mock_stdout):
        self.error_handler.print_colored("", "green")
        self.assertEqual("\033[32;40m\033[0m\n", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_special_characters(self, mock_stdout):
        self.error_handler.print_colored("!@#$%^&*()", "cyan")
        self.assertIn("!@#$%^&*()", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_multiline_text(self, mock_stdout):
        self.error_handler.print_colored("Line 1\nLine 2", "yellow")
        self.assertIn("Line 1\nLine 2", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_print_colored_case_insensitive_colors(self, mock_stdout):
        self.error_handler.print_colored("Test", "RED", "BLUE")
        self.assertIn("Test", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
