# IM PROGRESS - FOR SOME REASON MY OUTPUT IS A BUNCH OF CLUBS
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pickle

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

from utils_models import load_models
from utils_data_structures import col_prefixes


def create_goalkeepers_prediction():

    epl_teams_ = pd.read_csv('sorare/sorare_data/large_cleaned_sorare_data.csv')

    epl_teams_ = epl_teams_.fillna(0.0)

    drop_columns = ['Display_Name', 'First_Name','Last_Name','Player_Number', 'Position', 'Current_Club']

    epl_goalkeepers_df = epl_teams_[epl_teams_['Position'] == 'Goalkeeper']


    epl_goalkeepers_df = epl_goalkeepers_df.reset_index(drop=True)

    # Create X and y and split into training and testing sets
    target_column = 'So_5_Scores_9'
    columns_to_drop = [f'{col}_9' for col in col_prefixes]
    columns_to_drop.extend(drop_columns)

    # print(epl_goalkeepers_df.columns)
    # print(epl_goalkeepers_df.dtypes.value_counts())

    X_test_goalkeepers = epl_goalkeepers_df.drop(columns=columns_to_drop)
    y_test_goalkeepers = epl_goalkeepers_df[target_column]


    with open('sorare/sorare_models/goalkeepers_xgb_model.pkl', 'rb') as file:
        goalkeepers_xgb_model_loaded = pickle.load(file)
        # print("XGB Model loaded successfully!")
    with open('sorare/sorare_models/goalkeepers_lgbm_model.pkl', 'rb') as file:
        goalkeepers_lgbm_model_loaded = pickle.load(file)
        # print("LGBM Model loaded successfully!")
    with open('sorare/sorare_models/goalkeepers_elastic_model.pkl', 'rb') as file:
        goalkeepers_elastic_model_loaded = pickle.load(file)
        # print("Elastic Model loaded successfully!")

    print("GK Models saved successfully!")

    goalkeepers_xgb_predictions = goalkeepers_xgb_model_loaded.predict(X_test_goalkeepers)
    goalkeepers_lgbm_predictions = goalkeepers_lgbm_model_loaded.predict(X_test_goalkeepers)
    goalkeepers_elastic_predictions = goalkeepers_elastic_model_loaded.predict(X_test_goalkeepers)

    goalkeepers_xgb_predictions = np.clip(goalkeepers_xgb_predictions, 0, 100)
    goalkeepers_lgbm_predictions = np.clip(goalkeepers_lgbm_predictions, 0, 100)
    goalkeepers_elastic_predictions = np.clip(goalkeepers_elastic_predictions, 0, 100)

    y_test_goalkeepers_df = pd.DataFrame(y_test_goalkeepers)

    epl_goalkeepers_df['sorare_xgb_predictions'] = pd.Series(goalkeepers_xgb_predictions)
    epl_goalkeepers_df['sorare_lgbm_predictions'] = pd.Series(goalkeepers_lgbm_predictions)
    epl_goalkeepers_df['sorare_elastic_predictions'] = pd.Series(goalkeepers_elastic_predictions)

    epl_goalkeepers_df['sorare_predictions'] = epl_goalkeepers_df[['sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions']].mean(axis=1)

    epl_goalkeepers_df[['So_5_Scores_9','sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions']]

    y_true = epl_goalkeepers_df['So_5_Scores_9'].to_numpy()
    y_pred = epl_goalkeepers_df['sorare_predictions'].to_numpy()

    # Calculate RMSE
    print('Goalkeepers')
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f'MSE: {mean_squared_error(y_true, y_pred)}')
    print(f'RMSE: {rmse}')
    r2 = r2_score(y_true, y_pred)
    print(f'r2: {r2}')
    print('-'*60)

    saved_goalkeepers_df = epl_goalkeepers_df[['Display_Name', 'First_Name','Last_Name','Player_Number', 'Position', 'Current_Club','So_5_Scores_9','sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions', 'sorare_predictions']]
    saved_goalkeepers_df.to_csv('sorare/sorare_data/predictions/sorare_goalkeepers_predictions.csv', index=False)

    print('saved_goalkeepers_df')
