import pandas as pd
import json
import os

file_path = "/home/usic/Рабочий стол/парс цены.ods"
output_path = "/home/usic/.gemini/antigravity/scratch/kaspi/products.json"

try:
    # Read the ODS file
    # We assume the product names are in the first column
    df = pd.read_excel(file_path, engine="odf")
    
    # Clean the data: drop empty cells and take the first column
    products = df.iloc[:, 0].dropna().tolist()
    
    # Save to JSON
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully extracted {len(products)} products to {output_path}")
    print("Preview:", products[:5])
except Exception as e:
    print(f"Error: {e}")
