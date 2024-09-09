import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from utils.api_utils import fetch_market_data, extract_hisotry, filter_dataframe, Timer_Class

all_market_data = fetch_market_data()

# Convert to DataFrame
df = pd.DataFrame(all_market_data)
# price_history = df['Ownership_History'].apply(extract_hisotry) 
# df = pd.concat([df, price_history.fillna(0.0)], axis=1)

df_filtered = filter_dataframe(df)
print(df_filtered)

# Save to CSV or further process
df.to_csv('./sorare/sorare_data/test_sorare_market_data.csv', index=False)