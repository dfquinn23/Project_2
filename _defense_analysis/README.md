## Contents

### Directory Stucture
```
_defense_analysis/
├── data/
│   ├── cleaned/
│   │   ├── defender/
│   │   ├── forward/
│   │   ├── gameweeks/
│   │   ├── goalkeeper/
│   │   └── midfielder/
│   ├── processed/
│   └── raw/
│       ├── defender/
│       ├── forward/
│       ├── gameweeks/
│       ├── goalkeeper/
│       └── midfielder/
├── data_extraction/
└── notebooks/
```

### Data Extraction Scripts 
Overview of Scripts
1. ```01-my_bootstrap_static.py```
* Purpose: This script fetches the initial set of data from the FPL's bootstrap-static endpoint. It retrieves data about all players, teams, and creates a reference table of player names and their corresponding unique identifiers (element codes).
* Output: Three CSV files are generated:
    * bootstrap_static_players.csv: Contains detailed data about all players.
    * bootstrap_static_teams.csv: Contains information about the teams.
    * player_reference.csv: A reference table that maps player IDs to their first and last names.

2. ```02-my_element_summary.py```
* Purpose: This script fetches historical performance data for each player. It uses the player reference table to iterate through player IDs and fetches past season statistics.
* Output: Creates separate CSV files for each player in their respective position directories (e.g., goalkeeper, defender, midfielder, forward).

3. ```03-fixtures.py```
* Purpose: This script fetches the fixtures data from the FPL API. It retrieves information about upcoming matches, which can be useful for predictive modeling.
* Output: Generates a fixtures.csv file that contains the details of upcoming fixtures. It can also merge this data with the player reference to include player names.

4. ```04-gameweek.py```
* Purpose: This script retrieves live gameweek data, which includes player statistics for specific gameweeks. It merges this data with the player reference table to include player names and other identifying information.
* Output: Produces separate CSV files for each gameweek (e.g., gameweek_1.csv, gameweek_2.csv, etc.), stored in the gameweeks directory.

5. ```05-my_data_verification_and_cleaning.py```
* Purpose: Ensures that the data is consistent and verifies that every player ID in the reference table is accounted for in the cleaned data. It also merges relevant player information and flags any missing data.
* Output: Creates cleaned CSV files for each position (e.g., defender_cleaned.csv, goalkeeper_cleaned.csv) that are ready for analysis.

#### How to Execute the Scripts
To execute these scripts, follow the steps below in sequence:
1. Start by fetching the initial data using the 01-my_bootstrap_static.py script: ```python 01-my_bootstrap_static.py```
2. Next, run 02-my_element_summary.py to fetch player-specific historical data: ```python 02-my_element_summary.py```
3. Fetch fixture data using the 03-fixtures.py script: ```python 03-fixtures.py```
4. Run 05-gameweek.py to retrieve gameweek-specific data: ```python 05-gameweek.py```
5. Finally, clean and verify the data using 06-my_data_verification_and_cleaning.py: ```python 06-my_data_verification_and_cleaning.py```

### Example Code to Extract Names for Other Positions (e.g., Goalkeeper)
If you want to extract player names for other positions, such as goalkeepers, you can modify the 02-my_element_summary.py script or use the following standalone code snippet:
```
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

def process_position_data(position_id, base_url, save_dir):
    """Fetches and saves historical data for players of a given position ID."""
    # Load player reference data
    player_reference_df = pd.read_csv('../data/raw/player_reference.csv')
    
    # Filter for players of the given position
    position_players = player_reference_df[player_reference_df['element_type'] == position_id]
    
    for player_id in position_players['id']:
        player_url = f"{base_url}element-summary/{player_id}/"
        data = fetch_data(player_url)
        
        if data:
            history_past_df = pd.DataFrame(data['history_past'])
            os.makedirs(save_dir, exist_ok=True)
            history_past_df.to_csv(f'{save_dir}/player_summary_{player_id}.csv', index=False)
            print(f"Data saved for player ID {player_id} in {save_dir}")
        else:
            print(f"No data to save for player ID {player_id}.")

# Define the base URL for API
base_url = 'https://fantasy.premierleague.com/api/'

# Example to process goalkeepers
process_position_data(position_id=1, base_url=base_url, save_dir='../data/raw/goalkeeper')
```
Notes:
* position_id=1: This ID corresponds to goalkeepers (Change this to 2 for defenders, 3 for midfielders, and 4 for forwards).
* This code will fetch historical data for all goalkeepers and save them in the specified directory.


## About '_defense_analysis'

 ### 1. Data Directory (`data/`)

Current Season
- **gameweeks/**: Each of these files contains player performance data specific to a particular gameweek (week 1, week 2, and so on). These files capture various in-game metrics for each player's performance in the specified gameweek.
    - **Key Columns and Their Meaning**
    1. id: A unique identifier for each record, which might represent a unique entry in the dataset.
    2. stats: A dictionary-like column containing various statistics related to the player's performance in the gameweek. This includes:
        * minutes: The number of minutes the player was on the pitch.
        * goals_scored: Goals scored by the player.
        * assists: Assists made by the player.
        * clean_sheets: Whether the player kept a clean sheet (important for defenders and goalkeepers).
        * goals_conceded: Goals conceded while the player was on the field.
        * own_goals: Own goals scored by the player.
        * penalties_saved and penalties_missed: Relevant for goalkeepers and outfield players taking penalties.
        * yellow_cards and red_cards: Yellow and red cards received by the player.
        * saves: Number of saves made by the player (usually goalkeepers).
        * bonus: Bonus points awarded.
        * bps (Bonus Points System): A detailed metric used to allocate bonus points.
        * influence, creativity, threat, ict_index: Advanced performance metrics used in FPL scoring.
        * expected_goals, expected_assists, expected_goal_involvements, expected_goals_conceded: Expected statistics, likely based on advanced analytics and modeling.
    3. explain: A data structure that provides a breakdown of the points and stats contributing to the player's total for the gameweek. It includes:
        * fixture: The fixture ID related to the stats.
        * stats: A list of dictionaries detailing various performance metrics and their associated points, such as minutes, goals_scored, assists, etc.
        * first_name: The player's first name.
        * second_name: The player's last name or surname.
        * element_code: A unique identifier linking the player to their overall player profile. This code is crucial for merging data across different datasets.

- **fixtures.csv**: This file contains data about the scheduled matches (fixtures) in the league, including details about the teams playing, match outcomes, and match difficulty ratings.
    - **Key Columns and Their Meaning**
    1. code: A unique identifier for each fixture.
    2. event: The gameweek associated with the fixture.
    3. finished: A boolean indicating whether the fixture has been completed (TRUE or FALSE).
    4. finished_provisional: A boolean indicating provisional completion status (possibly used for live updates?).
    5. id: Another unique identifier (for internal or API use?).
    6. kickoff_time: The scheduled kickoff time and date for the fixture.
    7. minutes: The duration of the match, usually 90 for regular time.
    8. provisional_start_time: Indicates if the start time is provisional.
    9. started: A boolean indicating whether the match has started (TRUE or FALSE).
    10. team_a: The ID of the away team in the fixture.
    11. team_a_score: The number of goals scored by the away team.
    12. team_h: The ID of the home team in the fixture.
    13. team_h_score: The number of goals scored by the home team.
    14. stats: A complex column that contains nested data, capturing detailed match statistics such as goals scored, assists, yellow cards, etc., for both home and away teams.
    15. team_h_difficulty: A numerical representation of the match difficulty for the home team (a FPL derived stat).
    16. team_a_difficulty: Similar to team_h_difficulty, but for the away team.
    17. pulse_id: Another unique identifier (not clear how it is used).



Historical
- **defender/**: Contains CSV files with historical performance data for defenders.
- **forward/**: Contains CSV files with historical performance data for forwards.
- **goalkeeper/**: Contains CSV files with historical performance data for goalkeepers.
- **midfielder/**: Contains CSV files with historical performance data for midfielders.
- **bootstrap_static_players.csv**: CSV file containing static data about all players, including their ID, team, and position.
- **bootstrap_static_teams.csv**: CSV file containing static data about all teams in the league.

### 2. Data Extraction Directory (`data_extraction/`)

- Contains Python scripts that fetch and save data from the FPL API. Each script is focused on specific aspects of data collection, such as fetching player data or gameweek data.

### 3. Notebooks
- **04-defensive_metrics_feature_engineering.ipynb**: A Jupyter notebook for developing features and analyzing defensive player performance. 
- **03-defensive_metrics_exploration.ipynb**: A Jupyter notebook for initally exploring defensive metrics data. This notebook provides insights into various defensive statistics and how they relate to player performance.
- **02-defensive_metrics_extraction.ipynb**: A Jupyter notebook for initally extracting defensive metrics data. This notebook helps in filtering, cleaning, and processing the defensive data from raw API outputs.
- **01-fpl_data_exploration.ipynb**: A Jupyter notebook for exploring FPL data in general and discovery for each endpoint. This helped guide the initial analyses.
