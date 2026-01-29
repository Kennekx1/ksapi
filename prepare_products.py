
import pandas as pd
import json

file_path = "/home/usic/Рабочий стол/парс цены.ods"
output_products = "/home/usic/.gemini/antigravity/scratch/kaspi/products.json"

try:
    # Read without header
    df = pd.read_excel(file_path, engine="odf", header=None)
    
    # Assuming column 0 is the product name
    products = df[0].astype(str).tolist()
    
    # Filter out empty or nan
    products = [p for p in products if p and p.lower() != 'nan']
    
    print(f"Found {len(products)} products.")
    print(f"First 3: {products[:3]}")
    
    with open(output_products, "w", encoding="utf-8") as f:
        json.dump(products, f, ensure_ascii=False, indent=2)
        
    print(f"Saved to {output_products}")

except Exception as e:
    print(f"Error: {e}")
