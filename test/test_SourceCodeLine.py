import unittest
import sys
from pathlib import Path
from unittest.mock import patch
from io import StringIO

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.SourceCodeLine import SourceCodeLine

class TestSourceCodeLine(unittest.TestCase):
    def test_init_valid_line_number(self):
        line = SourceCodeLine(1, "TEST START 1000")
        self.assertEqual(line.line_number, 1)
        self.assertEqual(line.line_text, "TEST START 1000")
        self.assertEqual(line.label, '')
        self.assertEqual(line.opcode_mnemonic, '')
        self.assertEqual(line.operands, '')
        self.assertEqual(line.comment, '')
        self.assertIsNone(line.opcode_hex)
        self.assertEqual(line.address, 0x00000)
        self.assertIsNone(line.object_code)
        self.assertIsNone(line.instr_format)
        self.assertEqual(line.errors, [])
        self.assertEqual(line.instruction_length, 0)

    def test_init_string_line_number(self):
        line = SourceCodeLine("1", "TEST START 1000")
        self.assertEqual(line.line_number, 1)
        self.assertEqual(line.line_text, "TEST START 1000")

    def test_init_invalid_line_number(self):
        with self.assertRaises(ValueError) as context:
            SourceCodeLine("abc", "TEST START 1000")
        self.assertIn("Invalid line number", str(context.exception))

    def test_init_negative_line_number(self):
        line = SourceCodeLine(-1, "TEST START 1000")
        self.assertEqual(line.line_number, -1)

    def test_init_zero_line_number(self):
        line = SourceCodeLine(0, "TEST START 1000")
        self.assertEqual(line.line_number, 0)

    def test_init_empty_line_text(self):
        line = SourceCodeLine(1, "")
        self.assertEqual(line.line_text, "")

    def test_init_with_optional_parameters(self):
        line = SourceCodeLine(1, "TEST START 1000", "LABEL", "START", "1000", "; comment")
        self.assertEqual(line.line_number, 1)
        self.assertEqual(line.line_text, "TEST START 1000")
        self.assertEqual(line.label, '')
        self.assertEqual(line.opcode_mnemonic, '')
        self.assertEqual(line.operands, '')
        self.assertEqual(line.comment, '')

    def test_init_float_line_number(self):
        with self.assertRaises(ValueError) as context:
            SourceCodeLine(1.5, "TEST START 1000")
        self.assertIn("Invalid line number", str(context.exception))

if __name__ == '__main__':
    unittest.main()
