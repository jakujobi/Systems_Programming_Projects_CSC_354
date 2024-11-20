import unittest
import sys
from pathlib import Path
from unittest.mock import patch, mock_open, MagicMock
from io import StringIO

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.FileExplorer import FileExplorer

class TestFileExplorer(unittest.TestCase):
    def setUp(self):
        self.file_explorer = FileExplorer()

    @patch('Modules.FileExplorer.FileExplorer.find_file')
    @patch('Modules.FileExplorer.FileExplorer.open_file')
    @patch('Modules.FileExplorer.FileExplorer.read_file')
    def test_process_file_successful(self, mock_read, mock_open, mock_find):
        mock_find.return_value = "path/to/file.txt"
        mock_open.return_value = StringIO("test content")
        mock_read.return_value = ["line1", "line2"]
        
        result = self.file_explorer.process_file("test.txt")
        self.assertEqual(result, ["line1", "line2"])
        mock_find.assert_called_once_with("test.txt")
        mock_open.assert_called_once()
        mock_read.assert_called_once()

    @patch('Modules.FileExplorer.FileExplorer.find_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_file_not_found(self, mock_stdout, mock_find):
        mock_find.return_value = None
        result = self.file_explorer.process_file("nonexistent.txt")
        self.assertIsNone(result)
        self.assertIn("Error: Could not find the file", mock_stdout.getvalue())

    @patch('Modules.FileExplorer.FileExplorer.find_file')
    @patch('Modules.FileExplorer.FileExplorer.open_file')
    @patch('sys.stdout', new_callable=StringIO)
    def test_process_file_cannot_open(self, mock_stdout, mock_open, mock_find):
        mock_find.return_value = "path/to/file.txt"
        mock_open.return_value = None
        result = self.file_explorer.process_file("test.txt")
        self.assertIsNone(result)
        self.assertIn("Error: Could not open the file", mock_stdout.getvalue())

    @patch('Modules.FileExplorer.FileExplorer.find_file')
    def test_process_file_file_not_found_exception(self, mock_find):
        mock_find.side_effect = FileNotFoundError()
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.file_explorer.process_file("test.txt")
            self.assertIsNone(result)
            self.assertIn("File not found", mock_stdout.getvalue())

    @patch('Modules.FileExplorer.FileExplorer.find_file')
    def test_process_file_general_exception(self, mock_find):
        mock_find.side_effect = Exception("Unexpected error")
        with patch('sys.stdout', new_callable=StringIO) as mock_stdout:
            result = self.file_explorer.process_file("test.txt")
            self.assertIsNone(result)
            self.assertIn("An error occurred", mock_stdout.getvalue())

if __name__ == '__main__':
    unittest.main()
