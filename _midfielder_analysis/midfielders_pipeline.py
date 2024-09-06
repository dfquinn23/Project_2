# update_pipeline.py

import pandas as pd
import joblib
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.svm import SVR
from sklearn.model_selection import train_test_split

# Function to fetch and combine new and historical data
def fetch_and_combine_data():
    # Fetch new data
    new_data = pd.read_csv('../data/processed/new_elements_processed.csv')
    midfielders_new = new_data[new_data['element_type'] == 3]
    
    # Load historical data
    historical_data = pd.read_csv('Project_2/_defense_analysis/data/cleaned/midfielder/midfielder_cleaned.csv')
    
    # Select relevant features
    features = ['minutes', 'goals_scored', 'assists', 'clean_sheets', 'goals_conceded',
                'yellow_cards', 'red_cards', 'bonus', 'bps', 'influence', 'creativity',
                'threat', 'ict_index', 'expected_goals', 'expected_assists',
                'expected_goal_involvements', 'expected_goals_conceded']
    
    # Prepare datasets
    midfielders_new = midfielders_new[features].fillna(0)
    historical_data = historical_data[features].fillna(0)
    
    # Combine data
    combined_data = pd.concat([midfielders_new, historical_data], ignore_index=True)
    
    return combined_data

# Function to update models with combined data
def update_models():
    # Fetch combined data
    combined_data = fetch_and_combine_data()
    
    # Define target variable
    target = 'total_points'
    X = combined_data.drop(columns=[target])
    y = combined_data[target]
    
    # Split data into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Load and update models
    models = {
        'gradient_boosting': joblib.load('../models/gradient_boosting.pkl'),
        'random_forest': joblib.load('../models/random_forest.pkl'),
        'svm': joblib.load('../models/svm.pkl')
    }
    
    for model_name, model in models.items():
        # Retrain model with new data
        model.fit(X_train, y_train)
        
        # Save updated model
        joblib.dump(model, f'../models/{model_name}.pkl')
        print(f'Updated and saved {model_name} model.')

# Run the update
update_models()
