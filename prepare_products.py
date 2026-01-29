
import pandas as pd
import json
import os

file_path = "/home/usic/Рабочий стол/парс июнь.ods"
output_products = "/home/usic/.gemini/antigravity/scratch/kaspi/products.json"

try:
    # Read with header
    df = pd.read_excel(file_path, engine="odf")
    
    # Column is likely 'Название ' (with space based on inspect)
    # Let's try to find it dynamically to be safe, or hardcode if sure.
    col_name = 'Название '
    if col_name not in df.columns:
        # Try stripping
        df.columns = [c.strip() for c in df.columns]
        col_name = 'Название'
    
    if col_name in df.columns:
        products = df[col_name].astype(str).tolist()
    else:
        print(f"Column 'Название' not found. Available: {df.columns.tolist()}")
        products = []
    
    # Filter out empty or nan
    products = [p for p in products if p and p.lower() != 'nan']
    
    print(f"Found {len(products)} products.")
    print(f"First 3: {products[:3]}")
    
    with open(output_products, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    print(f"Saved to {output_products}")

except Exception as e:
    print(f"Error: {e}")
