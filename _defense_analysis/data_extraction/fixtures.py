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

def save_fixtures_data(data, save_dir):
    """Saves fixture data to the specified directory."""
    if data:
        fixtures_df = pd.DataFrame(data)
        # Create save directory if it doesn't exist
        os.makedirs(save_dir, exist_ok=True)
        # Save the fixtures data to a CSV file in the specified directory
        fixtures_df.to_csv(f'{save_dir}/fixtures.csv', index=False)
        print(f"Fixtures data saved in {save_dir}")
    else:
        print("No fixture data to save.")

def main():
    """Main function to fetch and save fixture data."""
    # Define the base URL for API
    base_url = 'https://fantasy.premierleague.com/api/'
    fixtures_url = f"{base_url}fixtures/"

    # Define save directory for fixtures data
    save_dir = '../data/raw/gameweeks'

    # Fetch fixtures data
    data = fetch_data(fixtures_url)

    # Save the fetched data
    save_fixtures_data(data, save_dir)

if __name__ == "__main__":
    main()
