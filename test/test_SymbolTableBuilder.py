import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock
from io import StringIO

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.Symbol_Table_Builder import *

class TestSymbolTableDriver(unittest.TestCase):
    def setUp(self):
        self.symbol_table_builder = SymbolTableDriver()
        self.test_symbols = [
            SymbolData("TEST1", "1000", True, False, True),
            SymbolData("TEST2", "2000", False, True, False),
            SymbolData("TEST3", "3000", True, True, True)
        ]

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_symbols_paginated_empty_list(self, mock_stdout):
        self.symbol_table_builder.display_symbols_paginated([])
        output = mock_stdout.getvalue()
        self.assertIn("Displaying found symbols", output)
        self.assertIn("Symbol", output)
        self.assertIn("Value", output)
        self.assertIn("RFlag", output)
        self.assertIn("IFlag", output)
        self.assertIn("MFlag", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_symbols_paginated_single_symbol(self, mock_stdout):
        single_symbol = [SymbolData("TEST", "1000", True, False, True)]
        self.symbol_table_builder.display_symbols_paginated(single_symbol)
        output = mock_stdout.getvalue()
        self.assertIn("TEST", output)
        self.assertIn("1000", output)
        self.assertIn("1", output)
        self.assertIn("0", output)

    @patch('sys.stdout', new_callable=StringIO)
    @patch.object(SymbolTableDriver, 'pressContinue')
    def test_display_symbols_paginated_pagination(self, mock_press_continue, mock_stdout):
        symbols = [SymbolData(f"SYM{i}", str(i*1000), True, False, True) for i in range(25)]
        self.symbol_table_builder.display_symbols_paginated(symbols)
        mock_press_continue.assert_called_once()

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_symbols_paginated_formatting(self, mock_stdout):
        self.symbol_table_builder.display_symbols_paginated(self.test_symbols)
        output = mock_stdout.getvalue()
        self.assertIn("┏", output)
        self.assertIn("┓", output)
        self.assertIn("┃", output)
        self.assertIn("┣", output)
        self.assertIn("┫", output)
        self.assertIn("┛", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_symbols_paginated_all_flags_true(self, mock_stdout):
        symbol = [SymbolData("ALL_TRUE", "5000", True, True, True)]
        self.symbol_table_builder.display_symbols_paginated(symbol)
        output = mock_stdout.getvalue()
        self.assertIn("ALL_TRUE", output)
        self.assertIn("5000", output)
        self.assertIn("1", output)

    @patch('sys.stdout', new_callable=StringIO)
    def test_display_symbols_paginated_all_flags_false(self, mock_stdout):
        symbol = [SymbolData("ALL_FALSE", "6000", False, False, False)]
        self.symbol_table_builder.display_symbols_paginated(symbol)
        output = mock_stdout.getvalue()
        self.assertIn("ALL_FALSE", output)
        self.assertIn("6000", output)
        self.assertIn("0", output)

if __name__ == '__main__':
    unittest.main()
