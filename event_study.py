import pandas as pd
import numpy as np

# 1. Load Data
def message(x): print(f"--- {x} ---")
message("Loading Datasets")

zhvi = pd.read_csv("BSB_Impact_Analysis/data/oki_zhvi_historical.csv")
distances = pd.read_csv("BSB_Impact_Analysis/data/zip_bsb_distances.csv")
announcements = [
    {"date": "2020-11-11", "event": "Bridge Fire/Shutdown"},
    {"date": "2022-12-29", "event": "$1.6B Federal Grant"},
    {"date": "2023-07-27", "event": "Contractor Award"},
    {"date": "2024-05-10", "event": "Final Federal Clearing"}
]

# 2. Preprocess ZHVI
id_vars = ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'State', 'City', 'Metro', 'CountyName']
zhvi_long = zhvi.melt(id_vars=id_vars, var_name='Date', value_name='Price')
zhvi_long['Date'] = pd.to_datetime(zhvi_long['Date'])
zhvi_long = zhvi_long.rename(columns={'RegionName': 'ZIP'})

# Join with distances
df = zhvi_long.merge(distances, on='ZIP', how='inner')

# 3. Analyze Events
def analyze_event(df, event_date, event_name, window_months=12):
    event_date = pd.to_datetime(event_date)
    start_date = event_date - pd.DateOffset(months=window_months)
    end_date = event_date + pd.DateOffset(months=window_months)
    
    event_df = df[(df['Date'] >= start_date) & (df['Date'] <= end_date)].copy()
    if event_df.empty: return None
    
    # Base price at event month
    base_dates = event_df[event_df['Date'] <= event_date]['Date']
    if base_dates.empty: return None
    base_date = base_dates.max()
    
    base_prices = event_df[event_df['Date'] == base_date][['ZIP', 'Price']].rename(columns={'Price': 'Base_Price'})
    event_df = event_df.merge(base_prices, on='ZIP')
    event_df['Price_Index'] = (event_df['Price'] / event_df['Base_Price']) * 100
    
    event_df['Zone'] = pd.cut(event_df['dist_meters'], 
                             bins=[0, 1600, 3200, 10000, 100000], 
                             labels=['<1 mile', '1-2 miles', '2-6 miles', 'Outer OKI'])
    
    summary = event_df.groupby(['Zone', 'Date'])['Price_Index'].mean().reset_index()
    return summary

all_event_summaries = []

message("Analyzing Major Events")
for event in announcements:
    summary = analyze_event(df, event['date'], event['event'])
    if summary is not None:
        summary['Event'] = event['event']
        all_event_summaries.append(summary)

if all_event_summaries:
    pd.concat(all_event_summaries).to_csv("BSB_Impact_Analysis/data/bsb_event_analysis.csv", index=False)

# 4. Long Term Trend
message("Calculating Long-Term Drift")
base_2020_date = '2020-01-31'
base_2020 = df[df['Date'] == base_2020_date][['ZIP', 'Price']].rename(columns={'Price': 'Price_Jan2020'})

df_long = df.merge(base_2020, on='ZIP')
df_long['Price_Growth_Since_2020'] = (df_long['Price'] / df_long['Price_Jan2020'] - 1) * 100

latest_date = df_long['Date'].max()
summary_long = df_long[df_long['Date'] == latest_date].groupby(pd.cut(df_long['dist_meters'], bins=[0, 1600, 3200, 10000, 100000]))['Price_Growth_Since_2020'].mean()

print("\nAverage Price Growth Since Jan 2020 to", latest_date.date())
print(summary_long)

summary_long.to_csv("BSB_Impact_Analysis/data/bsb_long_term_growth.csv")
