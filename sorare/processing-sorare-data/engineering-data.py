import pandas as pd

import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from utils.data_structures import english_prem_teams, col_prefixes

## working


cleaned_df = pd.read_csv('sorare/sorare_data/cleaned_sorare_data.csv')

# One-Hot Encoding for Current_Club
sorare_processed_df = pd.get_dummies(cleaned_df, columns=['Current_Club'], drop_first=True)

# Label Encode positions
label_encoder = LabelEncoder()
sorare_processed_df['Position'] = label_encoder.fit_transform(sorare_processed_df['Position'])

print(sorare_processed_df['Position'])

# Scaling ['Age', 'Average_Price', 'So_5_Average_Percent'] with Standard Scaler
scaler = StandardScaler()
standard_scaler_columns = ['Age', 'Average_Price', 'So_5_Average_Percent']

sorare_processed_df[standard_scaler_columns] = scaler.fit_transform(sorare_processed_df[standard_scaler_columns])

# scale So_5_Scores and Avg Price
# scaling with numpy since data distribution is highly skewed - can handle zeros
columns_to_transform = []
for col in col_prefixes:
    for index in range(0, 10):
        columns_to_transform.append(f'{col}_{index}')
sorare_processed_df[columns_to_transform] = np.log1p(sorare_processed_df[columns_to_transform])  # log1p is log(1 + x) which handles zeros

sorare_processed_df['Has_Issue_Bool'] = sorare_processed_df['Active_Injuries_Bool'] | sorare_processed_df['Active_Suspensions_Bool']
sorare_processed_df = sorare_processed_df.drop(columns=['Display_Name',	'First_Name','Last_Name', 'Player_Number', 'Active_Injuries_Bool', 'Active_Suspensions_Bool'])

# need to drop the last column for each of the col_prefixes and also the last 5 for the so_5_columns
# to avoid leakage
so_5_columns_to_drop = [f'{col_prefixes[0]}_{index}' for index in range(10, 15)]
columns_to_drop = [f'{col}_9' for col in col_prefixes]
columns_to_drop.extend(so_5_columns_to_drop)

print('Dropping columns:')
print(columns_to_drop)

features_data = sorare_processed_df.drop(columns=columns_to_drop)
target_data = sorare_processed_df['So_5_Scores_9']