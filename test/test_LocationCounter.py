import unittest
import sys
from pathlib import Path


repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.LocationCounter import LocationCounter

class TestLocationCounter(unittest.TestCase):
    def setUp(self):
        self.loc_counter = LocationCounter()

    def test_increment_by_valid_hex(self):
        self.loc_counter.increment_by_hexadecimal("A")
        self.assertEqual(self.loc_counter.current_address, 10)

    def test_increment_by_large_hex(self):
        self.loc_counter.increment_by_hexadecimal("FF")
        self.assertEqual(self.loc_counter.current_address, 255)

    def test_increment_by_zero_hex(self):
        initial_address = self.loc_counter.current_address
        self.loc_counter.increment_by_hexadecimal("0")
        self.assertEqual(self.loc_counter.current_address, initial_address)

    def test_increment_by_hex_with_spaces(self):
        self.loc_counter.increment_by_hexadecimal("  1F  ")
        self.assertEqual(self.loc_counter.current_address, 31)

    def test_increment_by_invalid_hex_raises_error(self):
        with self.assertRaises(ValueError):
            self.loc_counter.increment_by_hexadecimal("XYZ")

    def test_increment_by_empty_string_raises_error(self):
        with self.assertRaises(ValueError):
            self.loc_counter.increment_by_hexadecimal("")

    def test_increment_by_special_chars_raises_error(self):
        with self.assertRaises(ValueError):
            self.loc_counter.increment_by_hexadecimal("#$%")

    def test_multiple_increments(self):
        self.loc_counter.increment_by_hexadecimal("10")
        self.loc_counter.increment_by_hexadecimal("20")
        self.assertEqual(self.loc_counter.current_address, 48)

if __name__ == '__main__':
    unittest.main()
