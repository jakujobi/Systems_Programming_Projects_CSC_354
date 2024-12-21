import unittest
import sys
import os
from pathlib import Path

# Add parent directory to path to import modules
repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.Memory import Memory, MemoryUnit
from Modules.ErrorLogHandler import ErrorLogHandler

class TestMemoryUnit(unittest.TestCase):
    def setUp(self):
        self.logger = ErrorLogHandler()
        
    def test_memory_unit_initialization(self):
        unit = MemoryUnit(self.logger)
        self.assertFalse(unit.initialized)
        self.assertIsNone(unit.get_value())
        
    def test_memory_unit_value_setting(self):
        unit = MemoryUnit(self.logger)
        unit.set_value(0xFF)
        self.assertTrue(unit.initialized)
        self.assertEqual(unit.get_value(), 0xFF)
        
    def test_memory_unit_invalid_value(self):
        unit = MemoryUnit(self.logger)
        with self.assertRaises(ValueError):
            unit.set_value(256)
            
    def test_memory_unit_representation(self):
        unit = MemoryUnit(self.logger)
        self.assertEqual(repr(unit), "??")
        unit.set_value(0xAB)
        self.assertEqual(repr(unit), "AB")

class TestMemory(unittest.TestCase):
    def setUp(self):
        self.logger = ErrorLogHandler()
        self.memory = Memory(size=256, start_address=0x1000, logger=self.logger)
        
    def test_memory_initialization(self):
        self.assertEqual(self.memory.size, 256)
        self.assertEqual(self.memory.start_address, 0x1000)
        
    def test_address_translation(self):
        index = self.memory.translate_address(0x1000)
        self.assertEqual(index, 0)
        with self.assertRaises(ValueError):
            self.memory.translate_address(0x2000)
            
    def test_byte_operations(self):
        self.memory.write_byte(0x1000, 0xAA)
        self.assertTrue(self.memory.is_initialized(0x1000))
        self.assertEqual(self.memory.read_byte(0x1000), 0xAA)
        
    def test_multiple_byte_operations(self):
        test_data = bytes([0xDE, 0xAD, 0xBE, 0xEF])
        self.memory.write_bytes(0x1000, test_data)
        read_data = self.memory.read_bytes(0x1000, 4)
        self.assertEqual(read_data, [0xDE, 0xAD, 0xBE, 0xEF])
        
    def test_memory_dump(self):
        self.memory.write_byte(0x1000, 0xFF)
        dump = self.memory.get_dump(0x1000, 0x1010)
        self.assertIn("FF", dump)
        self.assertIn("01000", dump)
        
    def test_invalid_operations(self):
        with self.assertRaises(ValueError):
            self.memory.write_byte(0x1000, 256)
        with self.assertRaises(ValueError):
            self.memory.read_bytes(0x1000, -1)
            
    def test_uninitialized_read(self):
        value = self.memory.read_byte(0x1001)
        self.assertIsNone(value)
        
    def test_boundary_conditions(self):
        # Test at start of memory
        self.memory.write_byte(0x1000, 0x00)
        self.assertEqual(self.memory.read_byte(0x1000), 0x00)
        
        # Test at end of memory
        last_address = 0x1000 + 255
        self.memory.write_byte(last_address, 0xFF)
        self.assertEqual(self.memory.read_byte(last_address), 0xFF)

if __name__ == '__main__':
    unittest.main()
