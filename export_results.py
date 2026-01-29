import pandas as pd
import json
import os

json_path = "/home/usic/.gemini/antigravity/scratch/kaspi/kaspi_prices.json"
output_path = "/home/usic/Рабочий стол/результаты_парсинга.ods"

try:
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    # Flatten data for DataFrame
    rows = []
    for item in data:
        rows.append({
            "Запрос (из файла)": item["query"],
            "Найдено на Kaspi": item.get("match", "Не найдено"),
            "Цена (₸)": item.get("price"),
            "Кол-во продавцов": item.get("sellers"),
            "Ссылка": "https://kaspi.kz" + item.get("url", "") if item.get("url") else ""
        })
    
    df = pd.DataFrame(rows)
    
    # Save to ODS
    df.to_excel(output_path, engine="odf", index=False)
    
    print(f"Successfully saved results to {output_path}")
except Exception as e:
    print(f"Error: {e}")
