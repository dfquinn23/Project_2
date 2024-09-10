# This script ensures that all data sets are consistent, and verifies that every player ID
# in the reference table is accounted for in the cleaned data. Any missing data is flagged.


import pandas as pd
import os

# Function to check if a file is non-empty (greater than 1 byte)
def is_valid_csv(file_path):
    return os.path.getsize(file_path) > 1

# Function to clean and save data for a given position
def clean_data(position, reference_df):
    """
    Cleans the raw data files for a given position and merges them with the player reference data.
    Args:
        position (str): The position (e.g., 'defender', 'forward') to process.
        reference_df (pd.DataFrame): The player reference DataFrame.
    """
    # Define directories
    raw_dir = f'../raw/{position}/'
    cleaned_dir = f'../cleaned/{position}/'

    # Get a list of all files in the raw directory
    files = [f'{raw_dir}{file}' for file in os.listdir(raw_dir)]

    # Filter out empty or invalid files
    valid_files = [file for file in files if is_valid_csv(file)]

    # List of DataFrames for storing valid data
    dataframes = []

    # Read valid files and perform initial checks
    for file in valid_files:
        try:
            df = pd.read_csv(file)
            if not df.empty:  # Check if DataFrame is not empty
                dataframes.append(df)
                print(f"Added data from {file}")
            else:
                print(f"File {file} is empty or contains no usable data.")
        except pd.errors.EmptyDataError as e:
            print(f"EmptyDataError encountered while reading {file}: {e}")
        except Exception as e:
            print(f"Error encountered while reading {file}: {e}")

    # Concatenate all valid DataFrames into one
    if dataframes:
        combined_df = pd.concat(dataframes, ignore_index=True)
        print(f"Successfully concatenated {len(combined_df)} records for {position}.")
    else:
        print(f"No valid data found for {position}.")
        combined_df = pd.DataFrame()  # Create an empty DataFrame if no valid files are found

    # Check completeness by ensuring every player ID has a corresponding entry
    if 'element_code' in combined_df.columns:
        missing_ids = set(reference_df['element_code']) - set(combined_df['element_code'])
    else:
        missing_ids = set(reference_df['element_code'])

    if missing_ids:
        print(f"Warning: Missing data for player IDs: {missing_ids}")
    else:
        print("All player IDs are accounted for.")

    # Merge with player reference to include player names
    if 'element_code' in combined_df.columns:
        combined_df = combined_df.merge(reference_df, left_on='element_code', right_on='element_code', how='left')
        print("Player names merged successfully.")
    else:
        print("No 'element_code' column found in the combined data. Skipping merge.")

    # Create a unique identifier for each record (assuming season_name is available)
    if 'season_name' in combined_df.columns:
        combined_df['unique_id'] = combined_df['element_code'].astype(str) + '_' + combined_df['season_name'].astype(str)
    else:
        print("season_name not found in data; unique_id not created.")

    # Ensure the cleaned directory exists
    os.makedirs(cleaned_dir, exist_ok=True)

    # Save the cleaned data to a new CSV file
    cleaned_data_path = f'{cleaned_dir}{position}_cleaned.csv'
    combined_df.to_csv(cleaned_data_path, index=False)
    print(f"Cleaned data saved to {cleaned_data_path}")

def main():
    """Main function to verify and clean all position data."""
    # Load the player reference data
    reference_file_path = '../raw/player_reference.csv'
    if os.path.exists(reference_file_path):
        reference_df = pd.read_csv(reference_file_path)
        print("Player reference table loaded successfully.")
    else:
        print(f"Reference table not found at {reference_file_path}. Exiting.")
        return

    # List of positions to clean data for
    # positions = ['defender', 'forward', 'midfielder', 'goalkeeper', 'gameweeks']
    positions = ['defender', 'forward', 'midfielder', 'goalkeeper']


    # Iterate over each position and clean data
    for position in positions:
        print(f"Processing data for {position}...")
        clean_data(position, reference_df)

if __name__ == "__main__":
    main()
