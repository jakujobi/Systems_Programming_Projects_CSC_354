import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from Modules.AssemblerPass1 import AssemblerPass1
from Modules.ErrorLogHandler import ErrorLogHandler

class TestAssemblerPass1(unittest.TestCase):
    def setUp(self):
        self.logger = ErrorLogHandler()
        self.filename = "test_source.asm"
        self.assembler = AssemblerPass1(self.filename, logger=self.logger)

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_load_source_file_success(self, mock_read):
        mock_read.return_value = ["LINE1", "LINE2"]
        self.assembler.load_source_file()
        self.assertEqual(len(self.assembler.source_lines), 2)
        self.logger.log_action.assert_called_with("Read 2 lines from 'test_source.asm'.")

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_load_source_file_empty(self, mock_read):
        mock_read.return_value = []
        self.assembler.load_source_file()
        self.logger.log_error.assert_called_with("The file 'test_source.asm' is empty.")

    @patch('Modules.FileExplorer.FileExplorer.create_new_file_in_main')
    @patch('builtins.open', new_callable=MagicMock)
    def test_create_intermediate_file_success(self, mock_open, mock_create):
        mock_create.return_value = "path/to/intermediate.int"
        self.assembler.create_intermediate_file()
        mock_open.assert_called_with("path/to/intermediate.int", "w")

    @patch('Modules.FileExplorer.FileExplorer.create_new_file_in_main')
    def test_create_intermediate_file_failure(self, mock_create):
        mock_create.return_value = None
        self.assembler.create_intermediate_file()
        self.logger.log_error.assert_called_with("Failed to create intermediate file for 'test_source.asm'.")

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_process_source_lines_with_errors(self, mock_read):
        mock_read.return_value = ["LINE1", "LINE2"]
        self.assembler.process_source_lines(self.assembler.source_lines)
        self.assertTrue(self.logger.log_action.call_count > 0)

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_process_source_lines_stopping_on_error(self, mock_read):
        mock_read.return_value = ["LINE1", "LINE2"]
        self.assembler.stop_on_error = True
        self.assembler.process_source_lines(self.assembler.source_lines)
        self.assertTrue(self.logger.log_action.call_count > 0)

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_process_single_line_invalid_opcode(self, mock_read):
        mock_read.return_value = ["INVALID_OPCODE"]
        source_line = MagicMock()
        source_line.opcode_mnemonic = "INVALID_OPCODE"
        self.assembler.process_single_line(source_line)
        self.logger.log_error.assert_called_with("Invalid opcode mnemonic: 'INVALID_OPCODE'.")

    @patch('Modules.FileExplorer.FileExplorer.read_file_raw')
    def test_process_single_line_valid_opcode(self, mock_read):
        mock_read.return_value = ["VALID_OPCODE"]
        source_line = MagicMock()
        source_line.opcode_mnemonic = "VALID_OPCODE"
        self.assembler.process_single_line(source_line)
        self.logger.log_action.assert_called()

if __name__ == '__main__':
    unittest.main()
