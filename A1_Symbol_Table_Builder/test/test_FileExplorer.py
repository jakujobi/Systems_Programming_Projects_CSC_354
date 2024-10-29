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
    main()