## CSC 354 - Systems Programming
# Project: Literal table Builder
# File: johnA2.py

# Author: John Akujobi
# Date: 10/3/2024
# Description: 

"""
/******************************************************************************************
***                                                                                     ***
***  CSc 354 - Systems Programming                                                      ***
***  ASSIGNMENT : A2 - Literal Table and Expression Evaluator                           ***
***  INSTRUCTOR : George Hamer                                                          ***
***  DUE DATE : October 9, 2024                                                         ***
***                                                                                     ***
*******************************************************************************************
***  PROGRAM NAME : Literal Table and Expression Evaluator                              ***
***                                                                                     ***
***  DESCRIPTION :                                                                      ***
***      This program is designed to build a literal table and evaluate assembly        ***
***      language expressions as part of a SIC/XE assembler. It processes assembly      ***
***      language expressions, evaluates their operands, and manages literals in a      ***
***      linked list-based literal table. The program supports various addressing       ***
***      modes (direct, indirect, and immediate) and arithmetic operations              ***
***      (addition and subtraction) for a maximum of two operands per expression.       ***
***                                                                                     ***
***      The program performs the following tasks:                                      ***
***         - Reads symbols from a symbol table (SYMS.DAT)                              ***
***         - Parses expressions from an input file (EXPR.DAT or provided via CLI)      ***
***         - Evaluates the parsed expressions                                          ***
***         - Manages the literal table with insertion and updates                      ***
***         - Outputs the evaluation results, including relocatability flags            ***
***         - Displays detailed error messages for invalid expressions                  ***
***         - Handles paginated display for both expression results and literal table   ***
***                                                                                     ***
*******************************************************************************************
***  MODULES INCLUDED :                                                                 ***
***                                                                                     ***
***      - LiteralData : Represents a literal with its name, value, length, and         ***
***                     address.                                                        ***
***      - LiteralNode : Represents a node in the linked list containing literal data.  ***
***      - LiteralTableList : Manages the literal table using a linked list. Supports   ***
***                          insertion, searching, address updates, and display.        ***
***      - ErrorLogHandler : Handles logging of actions and errors, with support for    ***
***                          pagination of logs and errors.                             ***
***      - ExpressionParser : Responsible for parsing assembly expressions,             ***
***                          identifying literals, and validating operands.             ***
***      - ExpressionEvaluator : Evaluates parsed expressions and handles operand       ***
***                              calculations and relocatability.                       ***
***      - ExpressionResults : Formats and outputs evaluated expression results,        ***
***                            including the N-bit, I-bit, and X-bit flags.             ***
***      - LiteralTableDriver : Coordinates the overall flow of the program,            ***
***                            including building the symbol table, parsing and         ***
***                            evaluating expressions, and displaying results.          ***
***                                                                                     ***
*******************************************************************************************
***  INPUTS :                                                                           ***
***      - SYMS.DAT : Contains symbols and their attributes (symbol, value, rflag).     ***
***      - EXPR.DAT : File containing assembly language expressions (can be provided    ***
***                   via command line as an argument or defaults to EXPR.DAT).         ***
***                                                                                     ***
*******************************************************************************************
***  OUTPUTS :                                                                          ***
***      - Evaluated expression results with value, relocatability, N-bit, I-bit,       ***
***        and X-bit information displayed.                                             ***
***      - Literal table displayed with literal name, value, length, and address.       ***
***      - Error logs and action logs displayed with detailed error information.        ***
***                                                                                     ***
*******************************************************************************************
***  ERROR HANDLING :                                                                   ***
***      The program provides detailed error messages for various invalid operations,   ***
***      including unsupported symbols, invalid literals, and undefined symbols. It     ***
***      continues processing despite errors, logging them for user reference.          ***
***                                                                                     ***
******************************************************************************************/

"""

"""
/**************************************************************************************
*** NAME : John Akujobi                                                             ***
*** CLASS : CSc 354 - Systems Programming                                           ***
*** ASSIGNMENT : Assignment 2                                                       ***
*** DUE DATE : Oct, 2024                                                            ***
*** INSTRUCTOR : GEORGE HAMER                                                       ***
***************************************************************************************
*** DESCRIPTION :                                                                   ***
***                                                                                 ***
**************************************************************************************/
"""

# run 
# cd .\Systems_Programming_Projects_CSC_354\A2_Literal_Table; python johnA2.py Express.DAT

import sys
import os

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.Literal_Table_Builder import *


def main():
    """
    /***************************************************************************************
    ***  FUNCTION : main                                                                  ***
    ***  DESCRIPTION :                                                                    ***
    ***      Creates an instance of LiteralTableDriver and runs the program with the      ***
    ***      expression file passed via command line or default.                          ***
    ***************************************************************************************/
    """
    # Create an instance of LiteralTableDriver and run it
    expression_file = sys.argv[1] if len(sys.argv) > 1 else None
    driver = LiteralTableDriver()
    driver.run(expression_file)


if __name__ == "__main__":
    main()