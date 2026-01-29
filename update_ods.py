
import pandas as pd
import json
import os

file_path = "/home/usic/Рабочий стол/парс июнь.ods"
json_path = "/home/usic/.gemini/antigravity/scratch/kaspi/kaspi_prices.json"

try:
    # Read original ODS with header
    df = pd.read_excel(file_path, engine="odf")
    
    # Read scraped results
    with open(json_path, "r", encoding="utf-8") as f:
        scraped_data = json.load(f)
        
    print(f"Loaded {len(scraped_data)} results for {len(df)} rows.")

    # Prepare data lists
    prices = []
    sellers = []
    urls = []
    found_matches = []
    
    # Map results to rows. Ideally we should match by index if we preserved order.
    # The extraction script preserved order (tolist).
    
    for i in range(len(df)):
        if i < len(scraped_data):
            item = scraped_data[i]
            prices.append(item.get("price", ""))
            sellers.append(item.get("sellers", ""))
            urls.append("https://kaspi.kz" + item.get('url', '') if item.get('url') else "")
            found_matches.append(item.get("match", ""))
        else:
            prices.append("")
            sellers.append("")
            urls.append("")
            found_matches.append("")

    # Add new named columns
    df['Парс. Название'] = found_matches
    df['Цена (act)'] = prices
    df['Продавцы (act)'] = sellers
    df['Ссылка'] = urls
    
    # Save back to the same file WITH headers
    df.to_excel(file_path, engine="odf", index=False)
    print(f"Updated {file_path} with new columns.")
    
except Exception as e:
    print(f"Error: {e}")
