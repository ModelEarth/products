# Defaults to US - Combines all category csv into all.csv
# python create_allcsv.py 
# python create_allcsv.py IN

import csv
from pathlib import Path
import sys


def combine(folder_name: str) -> Path:
    base_dir = Path(__file__).resolve().parent
    folder = base_dir / "products-data" / folder_name
    out = folder / "all.csv"
    files = sorted([p for p in folder.glob("*.csv") if p.name != "all.csv"])

    if not files:
        raise FileNotFoundError(f"No csv files found in {folder}")

    header = None
    rows_written = 0

    with out.open("w", newline="", encoding="utf-8") as f_out:
        writer = None
        for path in files:
            with path.open("r", newline="", encoding="utf-8") as f_in:
                reader = csv.reader(f_in)
                try:
                    file_header = next(reader)
                except StopIteration:
                    continue

                if header is None:
                    header = file_header
                    writer = csv.writer(f_out)
                    writer.writerow(header)

                for row in reader:
                    writer.writerow(row)
                    rows_written += 1

    print(f"Wrote {rows_written} rows to {out}")
    return out


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "US"
    combine(folder)
