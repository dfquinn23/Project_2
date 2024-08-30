import pandas as pd
import requests

def fetch_data(url):
    """Fetches data from the FPL using HTTP GET request."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.json()  # Returns the JSON content as a dictionary
    except requests.RequestException as e:
        print(f"Failed to retrieve data from {url}. Error: {e}")
        return None

# Endpoint URL
base_url = 'https://fantasy.premierleague.com/api/'
fixtures_url = base_url + 'fixtures/'

# Fetch data
data = fetch_data(fixtures_url)

if data:
    # Convert data to DataFrame
    fixtures_df = pd.DataFrame(data)
    
    # Save DataFrame to CSV
    fixtures_df.to_csv('../data/fixtures.csv', index=False)
    print("Data saved to fixtures.csv")
else:
    print("No data to save.")
