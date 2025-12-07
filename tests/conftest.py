import sys
from pathlib import Path

# Ensure project root is on sys.path so tests can import the package
ROOT = Path(__file__).parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
