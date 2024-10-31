## CSC 354 - Systems Programming
# Project: Symbol Table Manager
# File: SYMBOL_TABLE.py
# Version 3.0
#   - Fixed teh arguement finding

# Author: John Akujobi
# Date: 9/8/2024
# Description: 

"""
/**************************************************************************************
*** NAME : John Akujobi                                                             ***
*** CLASS : CSc 354 - Systems Programming                                           ***
*** ASSIGNMENT : Assignment 1                                                       ***
*** DUE DATE : Sept 18, 2024                                                        ***
*** INSTRUCTOR : GEORGE HAMER                                                       ***
***************************************************************************************
*** DESCRIPTION :                                                                   ***
*** This program is a symbol table manager that reads symbols from a SYMS.DAT file, ***
***    inserts them into a binary search tree,                                      ***
***     and searches for symbols in the tree using a SEARCH.TXT file.               ***
*** The program uses a FileExplorer class to handle file operations,                ***
***     a Validator class to validate symbols, values, and RFlag,                   ***
***     and a SymbolTable class to manage the binary search tree.                   ***
*** The SymbolData class represents a symbol entry,                                 ***
***     and the SymbolNode class represents a node in the binary search tree.       ***
***     The SymbolTableDriver class manages the high-level logic                    ***
***          for file processingsymbol table management.                            ***
*** The program also includes a GUI file explorer using Tkinter for selecting files.***
*** The main function initializes and runs the SymbolTableDriver.                   ***
**************************************************************************************/
"""

import sys
import os
from pathlib import Path

repo_home_path = Path(__file__).resolve().parent.parent
sys.path.append(str(repo_home_path))
                
from Modules.test_symbol_table import SymbolTableDriver


def main():
    """
    /********************************************************************
    ***  FUNCTION : main                                              ***
    ***  CLASS  :                                                     ***
    *********************************************************************
    ***  DESCRIPTION: Main function that initializes and runs the app ***
    ***  with optional command-line arguments. If a search file is     ***
    ***  provided as a command-line argument, it is used; otherwise,   ***
    ***  the program asks for the search file name interactively.      ***
    ********************************************************************/
    """
    try:
        print("Welcome to the Symbol Table Manager!\n")
        driver = SymbolTableDriver()

        # Check if the user provided a command-line argument for the search file
        if len(sys.argv) > 1:
            search_file = sys.argv[1]  # First argument is the search file
            driver.run(search_file)
        else:
            # If no argument provided, fallback to interactive file finding
            driver.run()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    main()