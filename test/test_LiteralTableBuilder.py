import unittest
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))

from Modules.Literal_Table_Builder import *

class TestLiteralTableBuilder(unittest.TestCase):
    def setUp(self):
        self.builder = LiteralTableDriver()

    @patch('Modules.Literal_Table_Builder.LiteralTableList')
    def test_add_literal_success(self, mock_literal_table):
        mock_literal_table.return_value.add_literal.return_value = True
        result = self.builder.add_literal("LIT1", 10, 4)
        self.assertTrue(result)
        mock_literal_table.return_value.add_literal.assert_called_once_with("LIT1", 10, 4)

    @patch('Modules.Literal_Table_Builder.LiteralTableList')
    def test_add_literal_duplicate(self, mock_literal_table):
        mock_literal_table.return_value.add_literal.side_effect = ValueError("Duplicate literal")
        with self.assertRaises(ValueError) as context:
            self.builder.add_literal("LIT1", 10, 4)
        self.assertIn("Duplicate literal", str(context.exception))

    @patch('Modules.Literal_Table_Builder.ExpressionParser')
    def test_parse_expression_success(self, mock_parser):
        mock_parser.return_value.parse.return_value = (True, "Parsed Expression")
        result = self.builder.parse_expression("LIT1 + LIT2")
        self.assertTrue(result[0])
        self.assertEqual(result[1], "Parsed Expression")
        mock_parser.return_value.parse.assert_called_once_with("LIT1 + LIT2")

    @patch('Modules.Literal_Table_Builder.ExpressionParser')
    def test_parse_expression_invalid(self, mock_parser):
        mock_parser.return_value.parse.side_effect = ValueError("Invalid expression")
        with self.assertRaises(ValueError) as context:
            self.builder.parse_expression("LIT1 +")
        self.assertIn("Invalid expression", str(context.exception))

    @patch('Modules.Literal_Table_Builder.ExpressionEvaluator')
    def test_evaluate_expression_success(self, mock_evaluator):
        mock_evaluator.return_value.evaluate.return_value = 15
        result = self.builder.evaluate_expression("LIT1 + LIT2")
        self.assertEqual(result, 15)
        mock_evaluator.return_value.evaluate.assert_called_once_with("LIT1 + LIT2")

    @patch('Modules.Literal_Table_Builder.ExpressionEvaluator')
    def test_evaluate_expression_error(self, mock_evaluator):
        mock_evaluator.return_value.evaluate.side_effect = Exception("Evaluation error")
        with self.assertRaises(Exception) as context:
            self.builder.evaluate_expression("LIT1 + LIT2")
        self.assertIn("Evaluation error", str(context.exception))
        
    def test_literal_data_creation(self):
        """Test creation of LiteralData objects"""
        literal = LiteralData(name="=X'1A'", value="1A", length=1)
        self.assertEqual(literal.name, "=X'1A'")
        self.assertEqual(literal.value, "1A")
        self.assertEqual(literal.length, 1)
        self.assertIsNone(literal.address)

    def test_literal_data_invalid_input(self):
        """Test LiteralData validation"""
        with self.assertRaises(ValueError):
            LiteralData(name="", value="1A", length=1)
        with self.assertRaises(ValueError):
            LiteralData(name="=X'1A'", value="", length=1)
        with self.assertRaises(ValueError):
            LiteralData(name="=X'1A'", value="1A", length=0)

    @patch('Modules.Literal_Table_Builder.LiteralTableList')
    def test_literal_table_search(self, mock_literal_table):
        """Test searching for literals in the table"""
        mock_literal = LiteralData(name="=X'1A'", value="1A", length=1)
        mock_literal_table.return_value.search.return_value = mock_literal
        result = self.builder.literal_table.search("=X'1A'")
        self.assertEqual(result.name, "=X'1A'")

    @patch('Modules.Literal_Table_Builder.LiteralTableList')
    def test_update_literal_addresses(self, mock_literal_table):
        """Test updating literal addresses"""
        self.builder.literal_table.update_addresses(start_address=1000)
        mock_literal_table.return_value.update_addresses.assert_called_once_with(start_address=1000)

    def test_exists_by_value(self):
        """Test checking existence of literals by value"""
        literal = LiteralData(name="=X'1A'", value="1A", length=1)
        node = LiteralNode(literal)
        self.builder.literal_table.head = node
        self.assertTrue(self.builder.literal_table.exists_by_value("1A", "=X'1A'"))
        self.assertFalse(self.builder.literal_table.exists_by_value("2B", "=X'2B'"))

    @patch('Modules.Literal_Table_Builder.ErrorLogHandler')
    def test_error_logging(self, mock_log_handler):
        """Test error logging functionality"""
        error_message = "Test error message"
        self.builder.log_handler.log_error(error_message)
        mock_log_handler.return_value.log_error.assert_called_once_with(error_message)

    def test_expression_parser_initialization(self):
        """Test ExpressionParser initialization"""
        expressions = ["LIT1 + LIT2", "LIT3 - LIT4"]
        parser = ExpressionParser(expressions, self.builder.literal_table, self.builder.log_handler)
        self.assertEqual(parser.expressions_lines, expressions)

    def test_expression_evaluator_initialization(self):
        """Test ExpressionEvaluator initialization"""
        parsed_expressions = [{"expr1": "value1"}, {"expr2": "value2"}]
        evaluator = ExpressionEvaluator(parsed_expressions, None, self.builder.literal_table, self.builder.log_handler)
        self.assertEqual(evaluator.parsed_expressions, parsed_expressions)

if __name__ == '__main__':
    unittest.main()
