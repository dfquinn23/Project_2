## Contents

### Extracting the data

Summary of Steps
1. Create the necessary directories for organizing data.
2. Run bootstrap_static.py to get the foundational player and team data.
3. Run element_summary.py to fetch historical player data by type.
4. Run gameweek.py to fetch specific gameweek data, if needed.

### Instructions to Get Player Data

1. Create Necessary Directories:
Before running the scripts, make sure the directory structure is set up correctly.
    * ../data/goalkeeper
    * ../data/defender
    * ../data/midfielder
    * ../data/forward

2. Run bootstrap_static.py to Fetch Static Player Data:
The bootstrap_static.py script should be run first because it fetches the foundational player and team data needed for further analysis. This script will generate the 'bootstrap_static_players.csv' and 'bootstrap_static_teams.csv' files in the 'data/' directory.

* Navigate to the data_extraction/ directory and run the script:
```python bootstrap_static.py```

* This script fetches player and team data and saves it as:
    * ../data/bootstrap_static_players.csv
    * ../data/bootstrap_static_teams.csv


3. Run element_summary.py to Fetch Historical Player Data:
Once the static player data is available, use the 'element_summary.py' script to fetch historical player performance data. This script reads from 'bootstrap_static_players.csv' and fetches data for different player types (e.g., goalkeepers, defenders, midfielders, forwards).

* Run the script to fetch data for all player positions:
```python element_summary.py```

This script will:
* Read bootstrap_static_players.csv.
* Fetch historical performance data for players.
* Save the data in directories based on player type:
    - goalkeeper/ for goalkeepers
    - defender/ for defenders
    - midfielder/ for midfielders
    - forward/ for forwards


4. Run gameweek.py to Fetch Specific Gameweek Data:
Modify the gameweek.py script to specify the desired gameweek number:
* Open gameweek.py and set the gameweek_id variable:
```
# Specify the gameweek number
gameweek_id = 1
```

* Run the script to fetch the gameweek data:
```python gameweek.py```

This will save the gameweek data in the gameweeks/ directory.


## About _defense_analysis

 1. Data Directory (`data/`)

- **defender/**: Contains CSV files with historical performance data for defenders.
- **forward/**: Contains CSV files with historical performance data for forwards.
- **goalkeeper/**: Contains CSV files with historical performance data for goalkeepers.
- **midfielder/**: Contains CSV files with historical performance data for midfielders.
- **gameweeks/**: Contains CSV files with data for each gameweek.
- **bootstrap_static_players.csv**: CSV file containing static data about all players, including their ID, team, and position.
- **bootstrap_static_teams.csv**: CSV file containing static data about all teams in the league.
- **fixtures.csv**: CSV file containing data about fixtures, such as match dates, teams involved, and scores.

### 2. Data Extraction Directory (`data_extraction/`)

- Contains Python scripts that fetch and save data from the FPL API. Each script is focused on specific aspects of data collection, such as fetching player data or gameweek data.

### 3. Notebooks

- **defensive_metrics_exploration.ipynb**: A Jupyter notebook for initally exploring defensive metrics data. This notebook provides insights into various defensive statistics and how they relate to player performance.
- **defensive_metrics_extraction.ipynb**: A Jupyter notebook for initally extracting defensive metrics data. This notebook helps in filtering, cleaning, and processing the defensive data from raw API outputs.
- **fpl_data_exploration.ipynb**: A Jupyter notebook for exploring FPL data in general and discovery for each endpoint. This helped guide the initial analyses.
