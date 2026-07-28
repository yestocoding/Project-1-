import os
import glob
import pandas as pd

def load_and_summarize_datasets(data_dir="../data/raw"):
    if not os.path.exists(data_dir):
        data_dir = "data/raw"
        
    csv_files = glob.glob(os.path.join(data_dir, "*.csv"))
    print(f"Found {len(csv_files)} CSV datasets in '{data_dir}'.")
    
    dataframes = {}
    for file_path in sorted(csv_files):
        file_name = os.path.basename(file_path)
        df_name = os.path.splitext(file_name)[0]
        df = pd.read_csv(file_path)
        dataframes[df_name] = df
        print(f"Loaded {file_name}: Shape {df.shape}")
        
    return dataframes

def validate_fund_master_and_nav(data_dir="../data/raw"):
    
    if not os.path.exists(data_dir):
        data_dir = "data/raw"
        
    master_path = os.path.join(data_dir, "01_fund_master.csv")
    nav_path = os.path.join(data_dir, "02_nav_history.csv")
    
    if os.path.exists(master_path) and os.path.exists(nav_path):
        df_master = pd.read_csv(master_path)
        df_nav = pd.read_csv(nav_path)
        
        master_codes = set(df_master["scheme_code"].dropna().unique())
        nav_codes = set(df_nav["scheme_code"].dropna().unique())
        
        match_count = len(master_codes.intersection(nav_codes))
        total_master = len(master_codes)
        match_pct = (match_count / total_master) * 100 if total_master > 0 else 0
        
        print("\n" + "="*50)
        print(" DATA QUALITY SUMMARY")
        print("="*50)
        print(f"• Total Master Schemes: {total_master}")
        print(f"• NAV Schemes Matched: {match_count}")
        print(f"• Scheme Match Rate: {match_pct:.2f}%")
        print("="*50)

if __name__ == "__main__":
    load_and_summarize_datasets()
    validate_fund_master_and_nav()