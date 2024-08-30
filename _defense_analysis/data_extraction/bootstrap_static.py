import pandas as pd
import requests

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
    
    # Save DataFrames to CSV
    players_df.to_csv('../data/bootstrap_static_players.csv', index=False)
    teams_df.to_csv('../data/bootstrap_static_teams.csv', index=False)
    print("Data saved to bootstrap_static_players.csv and bootstrap_static_teams.csv")
else:
    print("No data to save.")