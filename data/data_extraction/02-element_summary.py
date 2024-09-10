# This script fetches player-specific data and uses the player reference table.

import pandas as pd
import requests
import os

def main():
    print("Current working directory:", os.getcwd())
    players_df = pd.read_csv('../raw/bootstrap_static_players.csv')
    print("Players DataFrame loaded successfully.")
    
def fetch_data(url):
    """Fetches data from the FPL URL using HTTP GET request."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return None

def process_player_data(player_id, base_url, save_dir):
    """Fetches and saves historical data for a given player ID in the specified directory."""
    player_url = f"{base_url}element-summary/{player_id}/"
    data = fetch_data(player_url)
    
    if data:
        history_past_df = pd.DataFrame(data['history_past'])
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        # Save the player's data to a CSV file in the appropriate directory
        history_past_df.to_csv(f'{save_dir}/player_summary_{player_id}.csv', index=False)
        print(f"Data saved for player ID {player_id} in {save_dir}")
    else:
        print(f"No data to save for player ID {player_id}.")

def main():
    """Main function to process player data based on position."""
    # Define the base URL for API
    base_url = 'https://fantasy.premierleague.com/api/'
    
    # Define the position mapping and corresponding save directories
    position_mapping = {
        1: ('Goalkeeper', '../raw/goalkeeper'),
        2: ('Defender', '../raw/defender'),
        3: ('Midfielder', '../raw/midfielder'),
        4: ('Forward', '../raw/forward')
    }
    
    # Read the player reference data from CSV
    players_df = pd.read_csv('../raw/bootstrap_static_players.csv')
    
    # Loop through the defined positions and process the players
    for element_type, (position_name, save_dir) in position_mapping.items():
        filtered_players_df = players_df[players_df['element_type'] == element_type]
        print(f"Processing {position_name}s, total players: {len(filtered_players_df)}")
        
        for player_id in filtered_players_df['id']:
            process_player_data(player_id, base_url, save_dir)

if __name__ == "__main__":
    main()
