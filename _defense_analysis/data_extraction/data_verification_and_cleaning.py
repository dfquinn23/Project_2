import pandas as pd
import os

# Function to check if a file is non-empty (greater than 1 byte)
def is_valid_csv(file_path):
    return os.path.getsize(file_path) > 1

# Function to clean and save data for a given position
def clean_data(position):
    # Define directories
    raw_dir = f'../data/raw/{position}/'
    cleaned_dir = f'../data/cleaned/{position}/'

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

    # Inspect the first few rows of the concatenated DataFrame
    print(combined_df.head())

    # Further cleaning if necessary, such as handling missing values
    # Example: Fill missing values with zero (if appropriate)
    # combined_df.fillna(0, inplace=True)

    # Ensure the cleaned directory exists
    os.makedirs(cleaned_dir, exist_ok=True)

    # Save the cleaned data to a new CSV file
    cleaned_data_path = f'{cleaned_dir}{position}_cleaned.csv'
    combined_df.to_csv(cleaned_data_path, index=False)
    print(f"Cleaned data saved to {cleaned_data_path}")

# List of positions to clean data for
positions = ['defender', 'forward', 'midfielder', 'goalkeeper', 'gameweeks']

# Iterate over each position and clean data
for position in positions:
    print(f"Processing data for {position}...")
    clean_data(position)
