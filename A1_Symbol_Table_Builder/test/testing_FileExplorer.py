# Import the FileExplorer class from SYMBOL_TABLE.py
from SYMBOL_TABLE import FileExplorer

def main():
    # Create an instance of FileExplorer
    file_explorer = FileExplorer()
    
    # Define the file name we are looking for
    file_name = "SYMS.DAT"
    
    # Process the file (SYMS.DAT) and get the cleaned lines
    lines = file_explorer.process_file(file_name)
    
    # If there are any lines, display them
    if lines:
        print("\nContents of the file 'SYMS.DAT':")
        for line in lines:
            print(line)
    else:
        print("Error: The file could not be processed or no valid lines were found.")
    
if __name__ == "__main__":
class TestFileExplorer:
    def test_read_line_with_comments(self):
        explorer = FileExplorer()
        test_line = "  SYMBOL ABC // This is a comment  "
        result = explorer._read_line_from_file(test_line)
        assert result == "SYMBOL ABC"

    def test_read_line_empty(self):
        explorer = FileExplorer()
        test_line = "     "
        result = explorer._read_line_from_file(test_line)
        assert result == ""

    def test_read_line_only_comment(self):
        explorer = FileExplorer()
        test_line = "// This is just a comment"
        result = explorer._read_line_from_file(test_line)
        assert result == ""

    def test_read_line_multiple_slashes(self):
        explorer = FileExplorer()
        test_line = "DATA XYZ /// Multiple slashes"
        result = explorer._read_line_from_file(test_line)    main()