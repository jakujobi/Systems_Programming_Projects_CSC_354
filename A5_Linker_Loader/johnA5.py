# johnA5.py

import os
import sys
from typing import List, Optional

from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import ErrorLogHandler
from Modules.LinkerLoader import LinkerLoader

def main():
    # Get all the input files from the command line and put them into a list.
    # They can be many files, from 1 to n.
    input_files = sys.argv[1:]
    
    # If no input files are provided, use a default list of files.
    if not input_files:
        input_files = ['prog1.obj', 'prog2.obj', 'prog3.obj']
    
    # Create an instance of the LinkerLoader class.
    linker_loader = LinkerLoader(input_files)
    linker_loader.run()

if __name__ == "__main__":
    main()