# This script fetches and saves fixture data.

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

def save_fixtures_data(data, save_dir, reference_df):
    """Saves fixture data to the specified directory and merges with player reference data."""
    if data:
        fixtures_df = pd.DataFrame(data)

        # Optional: Merge with player reference if relevant fields exist
        if 'element' in fixtures_df.columns and 'element_code' in reference_df.columns:
            fixtures_df = fixtures_df.merge(reference_df, left_on='element', right_on='element_code', how='left')
            print("Fixtures data merged with player reference data.")
        
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        # Save the fixtures data to a CSV file in the specified directory
        fixtures_df.to_csv(f'{save_dir}/fixtures.csv', index=False)
        print(f"Fixtures data saved in {save_dir}")
    else:
        print("No fixture data to save.")

def main():
    """Main function to fetch and save fixture data."""
    base_url = 'https://fantasy.premierleague.com/api/'
    fixtures_url = f"{base_url}fixtures/"
    save_dir = '../data/raw/gameweeks'
    
    # Fetch fixtures data
    data = fetch_data(fixtures_url)

    # Load the reference table
    reference_file_path = '../data/raw/player_reference.csv'
    if os.path.exists(reference_file_path):
        reference_df = pd.read_csv(reference_file_path)
        print("Reference table loaded.")
    else:
        print(f"Reference table not found at {reference_file_path}. Please ensure it is generated.")
        reference_df = pd.DataFrame()  # Empty DataFrame if not found
    
    # Save the fetched data
    save_fixtures_data(data, save_dir, reference_df)

if __name__ == "__main__":
    main()
