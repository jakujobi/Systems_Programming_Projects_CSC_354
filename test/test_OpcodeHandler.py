import unittest
import sys
from pathlib import Path

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.OpcodeHandler import OpcodeHandler

class TestOpcodeHandler(unittest.TestCase):
    def setUp(self):
        self.opcode_handler = OpcodeHandler()

    def test_empty_opcode_handler_initialization(self):
        self.assertEqual(len(self.opcode_handler.opcodes), 0)
        self.assertEqual(len(self.opcode_handler.directives), 0)

    def test_format_4_creation(self):
        self.assertTrue('+ADD' in self.opcode_handler.format_4)
        self.assertTrue('+LDA' in self.opcode_handler.format_4)
        self.assertFalse('+CLEAR' in self.opcode_handler.format_4)

    def test_get_format_for_format_4(self):
        self.assertEqual(self.opcode_handler.get_format('+ADD'), 4)
        self.assertEqual(self.opcode_handler.get_format('+LDA'), 4)

    def test_is_directive_validation(self):
        self.assertTrue(self.opcode_handler.is_directive('START'))
        self.assertTrue(self.opcode_handler.is_directive('END'))
        self.assertTrue(self.opcode_handler.is_directive('BYTE'))
        self.assertFalse(self.opcode_handler.is_directive('ADD'))
        self.assertFalse(self.opcode_handler.is_directive('INVALID'))

    def test_is_pseudo_op_validation(self):
        self.assertTrue(self.opcode_handler.is_pseudo_op('EXTDEF'))
        self.assertTrue(self.opcode_handler.is_pseudo_op('EQU'))
        self.assertFalse(self.opcode_handler.is_pseudo_op('START'))
        self.assertFalse(self.opcode_handler.is_pseudo_op('ADD'))

    def test_is_valid_format_4_validation(self):
        self.assertTrue(self.opcode_handler.is_valid_format_4('+ADD'))
        self.assertTrue(self.opcode_handler.is_valid_format_4('+LDA'))
        self.assertFalse(self.opcode_handler.is_valid_format_4('ADD'))
        self.assertFalse(self.opcode_handler.is_valid_format_4('+CLEAR'))

    def test_get_hex_values(self):
        self.assertEqual(self.opcode_handler.get_hex('ADD'), 0x18)
        self.assertEqual(self.opcode_handler.get_hex('LDA'), 0x00)
        self.assertEqual(self.opcode_handler.get_hex('STA'), 0x0C)

    def test_get_format_values(self):
        self.assertEqual(self.opcode_handler.get_format('ADD'), 3)
        self.assertEqual(self.opcode_handler.get_format('CLEAR'), 2)
        self.assertEqual(self.opcode_handler.get_format('FIX'), 1)

    def test_is_opcode_mnemonic_comprehensive(self):
        self.assertTrue(self.opcode_handler.is_opcode_mnemonic('ADD'))
        self.assertTrue(self.opcode_handler.is_opcode_mnemonic('START'))
        self.assertTrue(self.opcode_handler.is_opcode_mnemonic('EXTDEF'))
        self.assertTrue(self.opcode_handler.is_opcode_mnemonic('+ADD'))
        self.assertFalse(self.opcode_handler.is_opcode_mnemonic('INVALID'))
        self.assertFalse(self.opcode_handler.is_opcode_mnemonic('+INVALID'))

    def test_get_hex_invalid_opcode(self):
        with self.assertRaises(ValueError):
            self.opcode_handler.get_hex('INVALID')

    def test_get_format_invalid_opcode(self):
        with self.assertRaises(ValueError):
            self.opcode_handler.get_format('INVALID')


if __name__ == '__main__':
    unittest.main()