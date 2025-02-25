import sys
import pandas as pd
from pathlib import Path

def validate_csv(file_path: Path):
    try:
        df = pd.read_csv(file_path)
        print(f"✅ Valid CSV: {file_path}")
    except Exception as e:
        print(f"❌ Invalid CSV: {file_path}")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    file_path = Path(sys.argv[1])
    if not file_path.exists():
        print(f"⚠️ File not found: {file_path}")
        sys.exit(1)
    
    validate_csv(file_path)
