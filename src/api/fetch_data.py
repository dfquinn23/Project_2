# src/api/fetch_data.py
import requests
import pandas as pd
from datetime import datetime

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

def fetch_latest_gameweek_data():
    # Fetch the current gameweek
    bootstrap_url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
    bootstrap_response = requests.get(bootstrap_url)
    if bootstrap_response.status_code != 200:
        print(f"Failed to fetch bootstrap data: {bootstrap_response.status_code}")
        return None

    bootstrap_data = bootstrap_response.json()
    current_gameweek = next(gw for gw in bootstrap_data['events'] if gw['is_current'])
    current_gameweek_id = current_gameweek['id']

    # Fetch the latest gameweek data
    gameweek_url = f'https://fantasy.premierleague.com/api/event/{current_gameweek_id}/live/'
    gameweek_response = requests.get(gameweek_url)
    if gameweek_response.status_code != 200:
        print(f"Failed to fetch gameweek data: {gameweek_response.status_code}")
        return None

    gameweek_data = gameweek_response.json()
    
    # Convert to DataFrame
    gameweek_df = pd.DataFrame(gameweek_data['elements'])
    gameweek_df['gameweek'] = current_gameweek_id
    gameweek_df['season'] = '2024-2025'  # 2024-2025 season
    
    return gameweek_df

if __name__ == "__main__":
    # Fetch and save historical data
    json_data = fetch_fpl_data()
    if json_data:
        elements_df, elements_types_df, teams_df = build_dataframes(json_data)
        
        # Save dataframes as CSV files in the data/raw folder
        elements_df.to_csv('../../data/raw/elements.csv', index=False)
        elements_types_df.to_csv('../../data/raw/element_types.csv', index=False)
        teams_df.to_csv('../../data/raw/teams.csv', index=False)
        print("Historical data fetched and saved successfully!")

    # Fetch and save latest gameweek data
    latest_gameweek_df = fetch_latest_gameweek_data()
    if latest_gameweek_df is not None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        latest_gameweek_df.to_csv(f'../../data/raw/latest_gameweek_{timestamp}.csv', index=False)
        print(f"Latest gameweek data saved to latest_gameweek_{timestamp}.csv")
