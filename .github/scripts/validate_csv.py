import sys
import pandas as pd
from pathlib import Path

def validate_csv(file_path: Path, delimiter=";"):
    try:
        # Read just the first row to determine column count
        with file_path.open("r", encoding="utf-8") as f:
            header = f.readline().strip().split(delimiter)
            expected_columns = len(header)

        # Load entire CSV with explicit delimiter
        df = pd.read_csv(file_path, delimiter=delimiter, dtype=str, encoding="utf-8")

        # Check if all rows have the expected number of columns
        if any(df.apply(lambda row: len(row) != expected_columns, axis=1)):
            raise ValueError("Row count does not match expected column count")

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
