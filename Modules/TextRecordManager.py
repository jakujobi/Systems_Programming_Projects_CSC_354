import os
import sys
from pathlib import Path

repo_home_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(repo_home_path)

from Modules.ErrorLogHandler import *

class TextRecordManager:
    def __init__(self, logger: ErrorLogHandler = None):
        self.logger = logger or ErrorLogHandler()