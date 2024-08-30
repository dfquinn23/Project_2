import pandas as pd
import requests
import os

def fetch_data(url):
    """Fetches data from the FPL URL using HTTP GET request."""
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def process_player_data(player_id, base_url, save_dir):
    """Fetches and saves historical data for a given player ID in the specified directory."""
    player_url = f"{base_url}element-summary/{player_id}/"
    data = fetch_data(player_url)
    
    if data:
        history_past_df = pd.DataFrame(data['history_past'])
        # Create save directory if it doesn't exist
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)
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
        1: ('Goalkeeper', '../data/goalkeeper'),
        2: ('Defender', '../data/defender'),
        3: ('Midfielder', '../data/midfielder'),
        4: ('Forward', '../data/forward')
    }
    
    # Read the player data from CSV
    players_df = pd.read_csv('../data/bootstrap_static_players.csv')
    
    # Loop through the defined positions and process the players
    for element_type, (position_name, save_dir) in position_mapping.items():
        # Filter players based on the element_type
        filtered_players_df = players_df[players_df['element_type'] == element_type]
        print(f"Processing {position_name}s, total players: {len(filtered_players_df)}")
        
        # Fetch and save data for each player in the filtered list
        for player_id in filtered_players_df['id']:
            process_player_data(player_id, base_url, save_dir)

if __name__ == "__main__":
    main()
