import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
import numpy as np
from utils_data_structures import english_prem_teams, col_prefixes

df = pd.read_csv('sorare/sorare_data/test_sorare_market_data.csv')

# creating a groupby, but need to get ALL columns, to do that, need to create a list of columns with the appended index
agg_dict = {}
for prefix in col_prefixes:
    # Find all columns that match the current prefix
    matching_columns = [col for col in df.columns if col.startswith(prefix)]
    
    # Add these columns to the aggregation dictionary with 'mean' as the aggregation function
    for col in matching_columns:
        agg_dict[col] = 'mean'
agg_dict.update({
    'First_Name': 'first',
    'Last_Name': 'first',
    'Age': 'first',
    'Position': 'first',
    'Player_Number': lambda x: int(x.iloc[0]) if pd.notna(x.iloc[0]) else 0,
    'Current_Club': 'first',
    'Active_Injuries_Bool': 'first',
    'Active_Suspensions_Bool': 'first',
    'Num_Of_Owners': 'sum',
    'Average_Price': lambda x: round(x.mean(), 2),
})

grouped_df = df.groupby('Display_Name').agg(agg_dict).reset_index()


print(f"length Current Club before filtering by EPL teams: {len(grouped_df['Current_Club'].unique())}")
print('-' * 60)




grouped_df['So5_per_minute_8'] = (grouped_df['So_5_Scores_8'] / grouped_df['minsPlayed_8'])
grouped_df['So5_per_minute_7'] = (grouped_df['So_5_Scores_7'] / grouped_df['minsPlayed_7'])

action_columns = [
    'assistPenaltyWon',
    'bigChanceCreated',
    'duelWon',
    'effectiveClearance',
    'goalAssist',
    'goals',
    'interceptionWon',
    'lastManTackle',
    'penaltiesSaved',
    'penaltySave',
    'saves',
    'totalClearance',
    'totalPass',
]
idx = [6,7,8]

grouped_df['Total_Actions'] = 0
grouped_df['Total_Minutes'] = 0
for col in action_columns:
    grouped_df['Total_Actions'] += grouped_df[[f'{col}_{idx[0]}', f'{col}_{idx[1]}', f'{col}_{idx[2]}']].sum(axis=1) 

grouped_df['Total_Minutes'] = grouped_df[['minsPlayed_6', 'minsPlayed_7', 'minsPlayed_8']].sum(axis=1) / (90 * 3)

grouped_df['Actions_Per_Minute'] = round(grouped_df['Total_Actions'] / grouped_df[['minsPlayed_6', 'minsPlayed_7', 'minsPlayed_8']].sum(axis=1), 6)




grouped_df = grouped_df.drop(columns=['Total_Minutes'])

grouped_df['Points_Per_Action'] = np.where(
    (grouped_df[['So_5_Scores_6', 'So_5_Scores_7', 'So_5_Scores_8']].sum(axis=1) > 0) & 
    (grouped_df['Total_Actions'] > 0),  # Ensure both the scores and Total_Actions are greater than 0
    grouped_df['Total_Actions'] / grouped_df[['So_5_Scores_6', 'So_5_Scores_7', 'So_5_Scores_8']].sum(axis=1), 
    0  # Return 0 if any of the conditions are not met
)

min_columns = [f'minsPlayed_{index}' for index in range(9)]
grouped_df['Average_Minutes_Played'] = df[min_columns].mean(axis=1)
# creating a list of columns for 
so_5_columns = [f'{col_prefixes[0]}_{index}' for index in range(9)]
grouped_df['So_5_Points_Average'] = grouped_df[so_5_columns].mean(axis=1)
grouped_df = grouped_df.fillna(0.0)

# Getting rid of non-EPL clubs
sorare_filtered_df = grouped_df[grouped_df['Current_Club'].isin(english_prem_teams)]

print(f"length Current Club after filtering by EPL teams: {len(sorare_filtered_df['Current_Club'].unique())}")
print('-' * 60)
print(f"Clubs in current Dataframe:")
print(sorare_filtered_df["Current_Club"].unique())

# save cleaned df
sorare_filtered_df.to_csv('sorare/sorare_data/large_cleaned_sorare_data.csv', index=False)
grouped_df.to_csv('sorare/sorare_data/large_grouped_sorare_data.csv', index=False)
print(grouped_df.shape)