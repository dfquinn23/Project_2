# This script processes gameweek data and merges it with player reference data.

import pandas as pd
import requests
import os

def fetch_data(url):
    """Fetches data from the FPL URL using HTTP GET request."""
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return None

def save_gameweek_data(gameweek_id, base_url, save_dir, reference_df):
    """Fetches and saves data for a given gameweek ID and merges with player reference data."""
    gameweek_url = f"{base_url}event/{gameweek_id}/live/"
    data = fetch_data(gameweek_url)
    
    if data:
        elements = data.get('elements', [])
        gameweek_df = pd.DataFrame(elements)

        # Merge with player reference data if relevant fields exist
        if 'id' in gameweek_df.columns and 'id' in reference_df.columns:
            gameweek_df = gameweek_df.merge(reference_df, on='id', how='left')
            print(f"Gameweek {gameweek_id} data merged with player reference data.")
        else:
            print(f"No 'id' column found in gameweek data or reference data. Skipping merge.")

        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        gameweek_df.to_csv(f'{save_dir}/gameweek_{gameweek_id}.csv', index=False)
        print(f"Data saved to gameweek_{gameweek_id}.csv")
    else:
        print(f"No data to save for gameweek {gameweek_id}.")

def main():
    """Main function to fetch and save data for multiple gameweeks."""
    base_url = 'https://fantasy.premierleague.com/api/'
    save_dir = '../data/raw/gameweeks'
    
    # Specify gameweeks to fetch
    gameweeks_to_fetch = [1, 2, 3, 4]  # Example: Fetch data for gameweeks 1, 2, and 3
    
    # Load the reference table
    reference_file_path = '../data/raw/player_reference.csv'
    if os.path.exists(reference_file_path):
        reference_df = pd.read_csv(reference_file_path)
        print("Reference table loaded.")
    else:
        print(f"Reference table not found at {reference_file_path}. Please ensure it is generated.")
        reference_df = pd.DataFrame()  # Empty DataFrame if not found
    
    # Fetch and save data for each gameweek
    for gameweek_id in gameweeks_to_fetch:
        save_gameweek_data(gameweek_id, base_url, save_dir, reference_df)

if __name__ == "__main__":
    main()
