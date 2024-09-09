# Symbol Table Project Requirements
CSc 354 – Assignment #1 – Hamer – Due: 09-18-24
(Implement using python)
Write a complete module used to maintain the symbol table for the SIC/XE assembler:
- use a binary search tree implementation to store each symbol along with its associated attributes
- exportable binary search tree operations:
	- insert
	- search
	- view (create, destroy – non-class based)
Write a complete main/driver program that uses the symbol table module to process two text files:
- SYMS.DAT 
- Search file used to search the symbol table.

---
## Files
### SYMS.DAT
used to populate the symbol table.
- file format (each line):	SYMBOL     VALUE     RFLAG
- zero or more leading spaces in front of the SYMBOL attribute – ends with a colon (:)
- one or more leading spaces in front of the VALUE and RFLAG attributes.
 SYMS.DAT		//  File names are case sensitive in Linux as well as some languages
```text

ABCD:     50     True           //  Valid – insert ABCD and all attributes into symbol table  (*)

     B12_34:     -3     false       //  Valid – insert B12_ and all attributes into symbol table  (*)

  a1B2_c3_D4:   +45   true      //  Valid – insert A1B2 and all attributes into symbol table  (*)

     ABCD!:    33     true      //  ERROR – symbols contain letters, digits and underscore:  ABCD!

1234567890:     0     false     //  ERROR – symbols start with a letter:  1234567890

          ABCD_EF:  +100  TRUE  //  ERROR – symbol previously defined:  ABCD  (+)

a1234:  3.5   FALSE         //  ERROR – symbol a1234 invalid value:  3.5

     XYZ:     100     5         //  ERROR – symbol XYZ invalid rflag:  5

```
(*) no message displayed for valid symbols with valid attributes – set IFLAG to true – set MFLAG to false
(+) set MFLAG attribute to true for symbol ABCD

### Search File
search file
Used to search the symbol table
- search file name obtained from the command line.
- file format (each line):	SYMBOL
- zero or more leading spaces in front of the SYMBOL attribute – no colon
```text
ABCD					//  Found – display symbol ABCD and all attributes
     A1b2C3_xYz			//  Found – display symbol A1B2 and all attributes
CDEF					//  ERROR – CDEF not found in symbol table
          abc~def				//  ERROR – symbols contain letters, digits and underscore:  abc~def
a1b2c3d4e5f6				//  ERROR – symbols contain 10 characters maximum:  a1b2c3d4e5f6

```

### Test file
This file will be used as a test search file to test the project
It will have
- Illegal symbols
- Wrong characters coming first
- Double next lines
- Lots of leading space
- Above 9, 10, 11 characters for the Symbols
- Wrong info for the 

---
# Basic Algorithm
1.	read symbols and their attributes one line at a time from the file named SYMS.DAT.
	- invalid symbols and/or invalid symbol attributes are not inserted in the symbol table.
	- display the symbol along with a detailed error message.
	- valid symbols with valid attributes are inserted in the symbol table.
2.	read symbols one at a time from the search file.
	- if no file name was specified on the command line then prompt the user for the file name.
	- invalid symbol:	display the symbol along with a detailed error message.
	- valid symbol:		search for the symbol in the symbol table (significant portion only).
	- found:		display the symbol and its associated attributes.
	- not found:		display the symbol along with a detailed error message.
3.	perform an inorder traversal of the symbol table.
	- display all symbols and associated attributes in a tabular format using output formatting techniques.

- Open `SYMS.DAT`
- Read `SYMS.DAT`
- Validate data
- Insert into symbol table
- Handle duplicate symbols by setting `MFLAG` to be true
	- Only does this once for that symbol after there are more than one duplicate
- Ask the user for the search file
- Open the search file
- Read a line from the search file
- Clean the line
- Validate the line
- For each symbol, search the symbol table
- If found show the symbol and its attributes
- If not found, show an error message
---
## Symbol table
### SYMBOL
SYMBOL (also referred to as a label in assembly language programing)
- starts with a letter (A..Z, a..z).
- followed by letters (A..Z, a..z), digits (0..9), and the underscore (_).
- maximum of 10 characters in length in the source program – does not include the colon (:)
- only the first 4 characters are significant – only the first 4 characters are stored in the symbol table.
- not case sensitive (CSC_354, CSc_354, csc_354 – all the same symbol – stored as CSC_).
- Store them all as capital letters

### VALUE
- signed integer value (+, –, 0..9).
- Can be from -5000 to 5000
- 128 bit integer value
- An int type will work
### RFLAG (Boolean)
- false
- true
- not case sensitive.
### IFLAG (Boolean)
- indicates whether or not a symbol has been defined within the current control section (true for now).
### MFLAG (Boolean)
- indicates whether or not a symbol has been defined more than one time in the same control section.
- each valid symbol is inserted into the symbol table exactly one time (invalid symbols are never inserted).
### View the symbol table – required output order and format
```terminal
Symbol	Value	RFlag	IFlag	MFlag		//  Do not allow the data to scroll off of the screen
							//  Hold the output every 20 lines – Tera Term screen size
A1B2		45	1	1	0		//  Continue when user indicates to do so
ABCD		50	1	1	1
B12_		-3	0	1	0		//  Perform an inorder traversal of symbol table
```

### Notes and Suggestions
- Do NOT stop on error!!! Process all data in both files completely!!! Display detailed error messages!!!
- Check for errors in all symbols and all symbol attributes read from both files
	- Step #1		SYMBOL     VALUE     RFLAG
	- Step #2		SYMBOL
- Convert all values to one common format:
	- All symbols were converted to uppercase:		csc, CSC, CSc => CSC
	- All flag values were converted to Boolean values:	false => 0		true => 1

### Validation
These are the rules to validate it

---
## Other Requirements
- The module/program must use proper data abstraction techniques.
	- See the Assignment Requirements document on the course web site.
- All module/program files must be fully documented.
	- See the Documentation Requirements document on the course web site.
- All python files, modules and dependencies must be zipped together
	- Zip all files together and upload to D2L before class on the due date.
	- Python zip entire solution folder (containing project folder)
- All duplicate or near duplicate assignments will earn a grade of 0.
---
# Classes
## SymbolData Class
The `SymbolData` class can represent a single symbol entry in the table, storing:
- A symbol (processed as uppercase, only the first 4 characters are significant).
- Value (signed integer within the range of -5000 to 5000).
- RFlag (Boolean).
- IFlag (always true).
- MFlag (tracks if the symbol was inserted more than once).
```pseudo
class SymbolData:
    Attributes:
        symbol  # First 4 chars, uppercase
        value   # Integer value within -5000 to 5000
        rflag   # Boolean value
        iflag   # Boolean, always true initially
        mflag   # Boolean, indicates if a duplicate exists

    Constructor(symbol, value, rflag, iflag=True, mflag=False):
        Set attributes (symbol, value, rflag, iflag, mflag)
```
## Symbol Node
Each node in the BST will store a `Symbol`. The tree will be organized by the symbol's value (first 4 characters).
```python
class SymbolNode:
    def __init__(self, symbol_data):
        self.symbol_data = symbol_data #symbol object conatining data
        self.left = None # Left child node
        self.right = None # Right child node
```

## SymbolTable Class (BST Implementation)
- **Insert symbols** into the binary search tree (BST).
- **Search** for symbol name in the BST.
- **View** the entire table (in-order traversal).
- **Destroy** the entire table
- **Remove** a symbol
- **Tree Nodes**: Each node in the BST stores a `Symbol` object.
- **Duplication Handling**: If the symbol already exists, set the `MFlag` to `true`.
```pseudo
class SymbolTable:
    Methods:
	    insert(symbol_data)
		    Calles _insert to insert into the BST
        _insert(symbol, value, rflag):
			Does the actual insert implementation
			It should insert it into BST based on symbol's lexicographical order.
			check if symbol exists
                If duplicate:
                    Set MFlag to true.
                    This should only happen once

        search(symbol):
            exportable function to look up the symbol in the BST by calling the _search function
            If found:
                Return symbol data.
            Else:
                Return "Not Found" error.
        _search
	        Does the actual search implementation

        view():
            Perform an in-order traversal of the BST to display symbols and their attributes.
            Pause every 20 lines if there are more than 20 symbols (to prevent output scrolling).

        inorder_traversal(node, counter):
            Recursively traverse left, print current node, then traverse right.
            Increment the counter for each symbol printed.
            If counter == 20, pause for user input before continuing.

		destroy_symbol_table():
		    Set root to None (and let garbage collection handle cleanup)
```

## File Explorer
This finds the files and opens them, then reads their information
- **File Handling**: Open, read, and manage files.
- **Get Files from Command Line**: Prompt the user for file input.
- **System File Handling**: Interact with the file system for finding and opening files.
```pseudo
class FileExplorer:
    Methods:
        open_SYSM_file(file_path):
            Try to open the file in read mode
            Error handling for file not found, permission denied,  or file curropt
            If successful:
                Return file object
            Else:
                Return error

        read_SYSM(file):
            For each line in the file:
	            read the line
	            Cleans the leading space
				Skip empty lines
				ignore the // comments
	            add each line into a list of lines
	        return the list

		read_search_file():
            For each line in the file:
	            read the line
	            Cleans the leading space
				Skip empty lines
				ignore the // comments
	            add each line into a list of lines
	        return the list

        get_search_file_from_command():
            If file name is provided as a command line argument:
                Return file name
            Else:
                Prompt user for file name

        get_search_file_from_system():
            Open system file explorer and allow the user to select the file.
            Return selected file path
```

## Validator Class
- Perform validation checks on symbols, values, and flags
- Return error messages if the data does not meet criteria
- **Error reporting**: If a symbol fails validation, include detailed error messages like "Invalid symbol: must start with a letter" or "Invalid value: must be between -5000 and 5000."
Requirements
- **Validate symbol:**
    - Must start with a letter.
    - Can contain only letters, digits, and underscores.
    - Maximum of 10 characters.
    - Only the first 4 characters are significant.
- **Validate value:**
    - Must be a signed integer between -5000 and 5000.
- **Validate flags:**
    - `RFlag` should be either `true` or `false` (case-insensitive).
```pseudo
class Validator:
    Methods:
        validate_symbol(symbol):  # Check the symbol validity
            If symbol does not start with a letter or contains invalid characters:
                Return error message
            Check for reserved keywords or special characters

            If symbol length > 10:
                Return error message
            Return success

        validate_value(value):  # Check if value is in the valid range
	        It should chekc
            If value is not between -5000 and 5000:
                Return error message
            Check if it is an integer
            Check for wierd symbols
            Return success

        validate_rflag(rflag):  # check if it is a Boolean
            If rflag is not a boolean:
                Return error message
            Return success

		validate_syms_line (line)
			This validates the line from the syms file
			Separates each line into words/strings
			Checks if the line has exactly 3 parts
				Gives error message if not
			Extracts the symbol name, value, and rflag and places them into a local variables
			Convert using
				convert_symbol_to_SYMB(temp_symbol)
					then validate with validate_symbol
				convert_value_to_int(temp_value)
					then validate with validate_value
				convert_rflag_to_bool(temp_rflag)
					then validate with validate_rflag
			If all are successful
			returns it all as a SymbolData object

		validate_search_line
			This validates the line in question from the search file
			Separates each line into words/strings
			Checks if the line has exactly 1 parts
				Gives error message if not
			Extracts the symbol name, value, and rflag and places them into a local variables
			Convert using
				convert_symbol_to_SYMB(temp_symbol)
					then validate with validate_symbol
			If all are successful
			returns it all as a symbol

		convert_symbol_to_SYMB(temp_symbol)
			string temp_symbol
			It puts the symbol to uppercase
			It truncates it into the first 4
			string new_symbol
			return string new_symbol

		convert_rflag_to_bool(rflag)
			check if rflag is already a boolean
				if isinstance(rflag, bool):
			if its a string
				Convert to lowercase
				Check if rflag is 'true' or 'false'
					return true if rflag == true
					return false if rflag == false
					else it should raise error
			if its an integer, convert 1 to True and 0 to False
			If it matches none of the above, it should raise an error

		convert_value_to_int(value)
			check if it is already an integer, then return
			If it is a float, raise an error
			If it is a string, check if it has a "." and raise error
			if it is a string, attempt to convert to integer and return
			else raise a Typeerror

```


## SymbolTableLogic
This is the main algorithm
- **Coordinate** the file processing (SYMS.DAT and the search file).
- **Manage** the symbol table operations (insert, search, view).
- **Ensure Validation** is performed before any data is inserted into the symbol table.
- Centralize the main logic.
- Use the `FileExplorer` to read files.
- Use the `Validator` for checking input data.
- Call `SymbolTable` methods to manage the data.
- Add logging statements for each part
- This class actually does the whole program

```pseudo
class SymbolTableLogic:
    Attributes:
        symbol_table
        file_explorer
        validator

    Constructor():
        Initialize symbol_table as a new SymbolTable
        Initialize file_explorer as a new FileExplorer
        Initialize validator as a new Validator

    Methods:
        process_syms_file(file_path):
            Open and read the SYMS.DAT file using file_explorer
            Receive the list of lines from file_explorer (symbol list)
            For each line in the list:
                Validate them using the validate_syms_line
                If valid:
                    Insert the resulting symbol into symbol_table
                Else:
                    Print error message
            Do this until all the lines in the list are done

        process_search_file(file_path):
            Open and read the search file using file_explorer
            Receive the list of lines from file_explorer (searchlist)
            For each line in the list:
                Validate them using validate_search_line
                Search the symbol in the symbol_table
                If found:
                    Print symbol details
                Else:
                    Print "not found" error
            Do this until all the lines in the list are done

		def display_symbol_table():
		    counter = 0
		    For each symbol in the table:
		        If counter == 20:
		            Prompt user for input ("Press Enter to continue...")
		            Reset counter to 0
		        Print symbol details
		        Increment counter

		continue():
			This pauses the program and asks the user if they want to continue

		insert_symbol(symbol_table, symbol, value, rflag):
		    """
		    Standalone function to insert a symbol into the symbol table.
		    Calls the insert method of the SymbolTable class.
		    """
		    symbol_table.insert(symbol, value, rflag)

		search_symbol(symbol_table, symbol):
		    """
		    Standalone function to search for a symbol in the symbol table.
		    Calls the search method of the SymbolTable class.
		    """
		    return symbol_table.search(symbol)

		view_symbol_table(symbol_table):
		    """
		    Standalone function to view the contents of the symbol table.
		    Calls the in-order traversal (view) method of the SymbolTable class.
		    It displays the symbol data in a tabular format with pagination
		    (pauses every 20 lines using the continue() function).
		    """
		    symbol_table.view()

		destroy_symbol_table(symbol_table)

		remove_symbol(symbol_table, symbol):
```
## Main Program
- It simply **initializes** the `ProgramManager`.
- It **delegates** all the complex tasks (processing files, searching symbols, displaying the table) to the `ProgramManager`.
- Allow command-line arguments using the `argparse` module 

---
# 
---
# Question
- What file extension or format will the search file have

---
