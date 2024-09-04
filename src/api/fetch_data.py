# src/fetch_data.py
import requests
import pandas as pd

def fetch_fpl_data():
    url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    response = requests.get(url)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Failed to fetch data: {response.status_code}")
        return None

def build_dataframes(json_data):
    # Extract data and create DataFrames for elements, element_types and teams
    elements_df = pd.DataFrame(json_data['elements'])
    elements_types_df = pd.DataFrame(json_data['element_types'])
    teams_df = pd.DataFrame(json_data['teams'])
    
    return elements_df, elements_types_df, teams_df

if __name__ == "__main__":
    json_data = fetch_fpl_data()
    if json_data:
        elements_df, elements_types_df, teams_df = build_dataframes(json_data)
        
        # Save dataframes as CSV files in the data/raw folder
        elements_df.to_csv('../../data/raw/elements.csv', index=False)
        elements_types_df.to_csv('../../data/raw/element_types.csv', index=False)
        teams_df.to_csv('../../data/raw/teams.csv', index=False)
        print("Data fetched and saved successfully!")
