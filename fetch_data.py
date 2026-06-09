import pandas as pd
import requests
import os

ZILLOW_URL = "https://files.zillowstatic.com/research/public_csvs/zhvi/Zip_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
OUTPUT_PATH = "BSB_Impact_Analysis/data/zillow_zhvi_zip.csv"

def download_data():
    if not os.path.exists(OUTPUT_PATH):
        print("Downloading Zillow ZHVI data...")
        response = requests.get(ZILLOW_URL)
        with open(OUTPUT_PATH, 'wb') as f:
            f.write(response.content)
        print("Download complete.")
    else:
        print("File already exists.")

def filter_cincinnati_region():
    print("Filtering for Cincinnati MSA (OKI Region)...")
    df = pd.read_csv(OUTPUT_PATH)
    
    # State + County FIPS logic or explicit State + CountyName
    # OH: Hamilton, Butler, Clermont, Warren
    # KY: Boone, Kenton, Campbell
    # IN: Dearborn
    
    filters = [
        (df['State'] == 'OH') & (df['CountyName'].isin(['Hamilton County', 'Butler County', 'Clermont County', 'Warren County'])),
        (df['State'] == 'KY') & (df['CountyName'].isin(['Boone County', 'Kenton County', 'Campbell County'])),
        (df['State'] == 'IN') & (df['CountyName'] == 'Dearborn County')
    ]
    
    import functools
    import operator
    combined_filter = functools.reduce(operator.or_, filters)
    
    df_oki = df[combined_filter]
    df_oki.to_csv("BSB_Impact_Analysis/data/oki_zhvi_historical.csv", index=False)
    print(f"Filtered {len(df_oki)} zip codes.")

if __name__ == "__main__":
    download_data()
    filter_cincinnati_region()
