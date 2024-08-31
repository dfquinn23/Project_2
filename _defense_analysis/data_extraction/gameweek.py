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

def save_gameweek_data(gameweek_id, base_url, save_dir):
    """Fetches and saves data for a given gameweek ID."""
    gameweek_url = f"{base_url}event/{gameweek_id}/live/"
    data = fetch_data(gameweek_url)
    
    if data:
        elements = data.get('elements', [])
        gameweek_df = pd.DataFrame(elements)
        
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        
        gameweek_df.to_csv(f'{save_dir}/gameweek_{gameweek_id}.csv', index=False)
        print(f"Data saved to gameweek_{gameweek_id}.csv")
    else:
        print(f"No data to save for gameweek {gameweek_id}.")

def main():
    """Main function to fetch and save data for multiple gameweeks."""
    base_url = 'https://fantasy.premierleague.com/api/'
    save_dir = '../data/raw/gameweeks'  # Updated directory to save gameweek data

    # Specify the gameweeks to process
    gameweeks_to_fetch = [1, 2, 3]  # Example: Fetch data for gameweeks 1, 2, and 3

    # Loop through each gameweek ID and fetch/save the data
    for gameweek_id in gameweeks_to_fetch:
        save_gameweek_data(gameweek_id, base_url, save_dir)

if __name__ == "__main__":
    main()
