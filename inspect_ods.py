
import pandas as pd
import sys

# Install odfpy if needed, usually pandas requires it for ods
# But we assume the environment has it based on previous successful runs or we will find out.

file_path = "/home/usic/Рабочий стол/парс цены.ods"

try:
    df = pd.read_excel(file_path, engine="odf")
    print("Columns found:", df.columns.tolist())
    print("\nFirst 5 rows:")
    print(df.head())
except Exception as e:
    print(f"Error reading ODS: {e}")
