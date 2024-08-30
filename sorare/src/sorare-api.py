import pandas as pd
from apiutils import fetch_market_data, extract_hisotry, filter_dataframe, Timer_Class

all_market_data = fetch_market_data()

# Convert to DataFrame
df = pd.DataFrame(all_market_data)
price_history = df['Ownership_History'].apply(extract_hisotry)
df = pd.concat([df, price_history.fillna(0.0)], axis=1)

df_filtered = filter_dataframe(df)

# Save to CSV or further process
df.to_csv('./sorare/sorare_data/sorare_market_data.csv', index=False)
df_filtered.to_csv('./sorare/sorare_data/sorare_market_data_filtered.csv', index=False)