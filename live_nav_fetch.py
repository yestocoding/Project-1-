import os
import requests
import pandas as pd

def fetch_key_schemes_nav():
    key_schemes = {
       119551: "SBI Bluechip",
    120503: "ICICI Bluechip",
    118632: "Nippon Large Cap",
    119092: "Axis Bluechip",
    120841: "Kotak Bluechip",
    }

    combined_data = []

    for scheme_code, scheme_name in key_schemes.items():
        url = f"https://api.mfapi.in/mf/{scheme_code}"
        print(f"Fetching data for: {scheme_name} ({scheme_code})...")
        
        res = requests.get(url)
        if res.status_code == 200:
            json_data = res.json()
            meta = json_data.get("meta", {})
            nav_list = json_data.get("data", [])

            for item in nav_list:
                item["scheme_code"] = scheme_code
                item["scheme_name"] = meta.get("scheme_name", scheme_name)
                item["fund_house"] = meta.get("fund_house", "")
                item["scheme_category"] = meta.get("scheme_category", "")
                combined_data.append(item)
        else:
            print(f" Failed to fetch code {scheme_code}: HTTP {res.status_code}")

    df = pd.DataFrame(combined_data)
    
    # Reorder columns
    cols = ["scheme_code", "scheme_name", "fund_house", "scheme_category", "date", "nav"]
    df = df[cols]

    output_dir = "../data/raw" if os.path.exists("../data/raw") else "data/raw"
    os.makedirs(output_dir, exist_ok=True)
    
    csv_path = os.path.join(output_dir, "12_key_5_schemes_nav.csv")
    df.to_csv(csv_path, index=False)
    print(f" Successfully saved {len(df)} records to {csv_path}")

if __name__ == "__main__":
    fetch_key_schemes_nav()