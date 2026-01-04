import sys
import os

# Add the parent directory to the path so we can see 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import your existing app
from backend.main import app