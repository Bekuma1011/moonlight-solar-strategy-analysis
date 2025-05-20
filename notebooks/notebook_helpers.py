import sys
import os
from pathlib import Path

def add_project_root_to_path():
    """
    Add project root to Python path for notebooks.
    Prints status messages to confirm the operation.
    """
    project_root = str(Path(__file__).parent.parent)
    if project_root not in sys.path:
        sys.path.append(project_root)
        print("Added project root to Python path")
    else:
        print("Project root already in Python path")


add_project_root_to_path()
    