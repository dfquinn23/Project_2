import pandas as pd
from utils.data_structures import english_prem_teams, col_prefixes

df = pd.read_csv('sorare/sorare_data/sorare_market_data.csv')

df.fillna(0.0)

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

# Getting rid of non-EPL clubs
sorare_filtered_df = grouped_df[grouped_df['Current_Club'].isin(english_prem_teams)]

print(f"length Current Club after filtering by EPL teams: {len(sorare_filtered_df['Current_Club'].unique())}")
print('-' * 60)
print(f"Clubs in current Dataframe:")
print(sorare_filtered_df["Current_Club"].unique())

# replacing NaN values with 0.0
sorare_filtered_df = sorare_filtered_df.fillna(0.0)

# creating a list of columns for 
so_5_columns = [f'{col_prefixes[0]}_{index}' for index in range(9)]
sorare_filtered_df['So_5_Average_Percent'] = sorare_filtered_df[so_5_columns].mean(axis=1)

# save cleaned df
sorare_filtered_df.to_csv('sorare/sorare_data/cleaned_sorare_data.csv', index=False)
grouped_df.to_csv('sorare/sorare_data/grouped_sorare_data.csv', index=False)