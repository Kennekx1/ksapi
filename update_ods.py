
import pandas as pd
import json

file_path = "/home/usic/Рабочий стол/парс цены.ods"
json_path = "/home/usic/.gemini/antigravity/scratch/kaspi/kaspi_prices.json"

try:
    # Read original ODS
    df = pd.read_excel(file_path, engine="odf", header=None)
    
    # Read scraped results
    with open(json_path, "r", encoding="utf-8") as f:
        scraped_data = json.load(f)
        
    # Ensure lengths match
    if len(df) != len(scraped_data):
        print(f"Warning: File has {len(df)} rows, but scrape results have {len(scraped_data)} items.")
        print("Will attempt to append by index order up to the shorter length.")
        
    # Prepare data lists
    found_names = []
    prices = []
    sellers = []
    urls = []
    
    for item in scraped_data:
        found_names.append(item.get("match", ""))
        prices.append(item.get("price", ""))
        sellers.append(item.get("sellers", ""))
        urls.append("https://kaspi.kz" + item.get('url', '') if item.get('url') else "")
        
    # If the df is longer than results, pad with empty string
    while len(found_names) < len(df):
        found_names.append("")
        prices.append("")
        sellers.append("")
        urls.append("")

    # Add new columns (using next available indices)
    # The dataframe has numeric columns 0, 1...
    next_col = len(df.columns)
    
    df[next_col] = found_names
    df[next_col + 1] = prices
    df[next_col + 2] = sellers
    df[next_col + 3] = urls
    
    # Optional: Rename columns if we used names, but since we had no headers, we keep it as is.
    # We might want to save WITH headers now to make it readable?
    # User said "add quotes there" (paraphrasing "prices"), imply modifying existing structure.
    # If I add headers now, I might shift the original data down if there were no headers.
    # Let's keep it headerless but the user will see new columns.
    
    # Wait, the user might want headers now.
    # The first row was: "Today Parfum..." (a product). So definitely no headers currently.
    # If I just append columns, row 0 gets row 0's price. Correct.
    
    # Save back to the same file
    df.to_excel(file_path, engine="odf", index=False, header=False)
    print(f"Updated {file_path} with new data.")
    
except Exception as e:
    print(f"Error: {e}")
