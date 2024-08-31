import pandas as pd
import requests
import os

def fetch_data(url):
    """Fetches data from the FPL URL using HTTP GET request."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()  # Returns the JSON content as a dictionary
    except requests.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return None

# Endpoint URL
base_url = 'https://fantasy.premierleague.com/api/'
bootstrap_url = base_url + 'bootstrap-static/'

# Fetch data
data = fetch_data(bootstrap_url)

if data:
    # Convert relevant data to DataFrame
    players_df = pd.DataFrame(data['elements'])
    teams_df = pd.DataFrame(data['teams'])

    # Define paths for saving data
    raw_data_dir = '../data/raw/'
    players_file_path = os.path.join(raw_data_dir, 'bootstrap_static_players.csv')
    teams_file_path = os.path.join(raw_data_dir, 'bootstrap_static_teams.csv')

    # Ensure the raw data directory exists
    os.makedirs(raw_data_dir, exist_ok=True)

    # Save DataFrames to CSV in the raw directory
    players_df.to_csv(players_file_path, index=False)
    teams_df.to_csv(teams_file_path, index=False)
    print(f"Data saved to {players_file_path} and {teams_file_path}")
else:
    print("No data to save.")
