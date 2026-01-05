import sys
import os

# Get the current directory (api folder)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Go up one level to the Root folder
root_dir = os.path.dirname(current_dir)

# Define the Backend folder path
backend_dir = os.path.join(root_dir, 'backend')

# Add BOTH to the System Path
sys.path.append(root_dir)
sys.path.append(backend_dir) # <--- This is the magic fix.

# Now Python can find 'db' because we added 'backend' to the path.
from backend.main import app