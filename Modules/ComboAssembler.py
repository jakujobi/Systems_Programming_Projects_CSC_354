
import os
import sys
from typing import List
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.AssemblerPass1 import AssemblerPass1
from Modules.AssemblerPass2 import AssemblerPass2

class ComboAssembler:
    """
    Assembles a source program in two passes: Pass 1 and Pass 2.
    """
    def __init__(self, source_file):
        self.source_file = source_file
        self.pass1 = AssemblerPass1(self.source_file)
        self.pass2 = AssemblerPass2(self.source_file)
    
    def assemble(self):
        self.pass1.run()
        self.pass2.run()
        
        