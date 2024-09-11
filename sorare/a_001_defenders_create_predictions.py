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

def create_defenders_prediction():
    """
    creates dataframe for epl teams
    filters for defenders
    splits data

    loads saved defender models

    saves predictions
    """

    epl_teams_ = pd.read_csv('sorare/sorare_data/large_cleaned_sorare_data.csv')

    epl_teams_ = epl_teams_.fillna(0.0)

    drop_columns = ['Display_Name', 'First_Name','Last_Name','Player_Number', 'Position', 'Current_Club']

    epl_defenders_df = epl_teams_[epl_teams_['Position'] == 'Defender']

    epl_defenders_df = epl_defenders_df.reset_index(drop=True)

    # Create X and y and split into training and testing sets
    target_column = 'So_5_Scores_9'
    columns_to_drop = [f'{col}_9' for col in col_prefixes]
    columns_to_drop.extend(drop_columns)

    # print(epl_defenders_df.columns)
    # print(epl_defenders_df.dtypes.value_counts())

    X_test_defenders = epl_defenders_df.drop(columns=columns_to_drop)
    y_test_defenders = epl_defenders_df[target_column]


    with open('sorare/sorare_models/defenders_xgb_model.pkl', 'rb') as file:
        defenders_xgb_model_loaded = pickle.load(file)
        # print("XGB Model loaded successfully!")
    with open('sorare/sorare_models/defenders_lgbm_model.pkl', 'rb') as file:
        defenders_lgbm_model_loaded = pickle.load(file)
        # print("LGBM Model loaded successfully!")
    with open('sorare/sorare_models/defenders_elastic_model.pkl', 'rb') as file:
        defenders_elastic_model_loaded = pickle.load(file)
        # print("Elastic Model loaded successfully!")

    defenders_xgb_predictions = defenders_xgb_model_loaded.predict(X_test_defenders)
    defenders_lgbm_predictions = defenders_lgbm_model_loaded.predict(X_test_defenders)
    defenders_elastic_predictions = defenders_elastic_model_loaded.predict(X_test_defenders)

    defenders_xgb_predictions = np.clip(defenders_xgb_predictions, 0, 100)
    defenders_lgbm_predictions = np.clip(defenders_lgbm_predictions, 0, 100)
    defenders_elastic_predictions = np.clip(defenders_elastic_predictions, 0, 100)

    y_test_defenders_df = pd.DataFrame(y_test_defenders)

    epl_defenders_df['sorare_xgb_predictions'] = pd.Series(defenders_xgb_predictions)
    epl_defenders_df['sorare_lgbm_predictions'] = pd.Series(defenders_lgbm_predictions)
    epl_defenders_df['sorare_elastic_predictions'] = pd.Series(defenders_elastic_predictions)

    epl_defenders_df['sorare_predictions'] = epl_defenders_df[['sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions']].mean(axis=1)

    epl_defenders_df[['So_5_Scores_9','sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions']]

    y_true = epl_defenders_df['So_5_Scores_9'].to_numpy()
    y_pred = epl_defenders_df['sorare_predictions'].to_numpy()

    # Calculate RMSE
    print('Defenders')
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    print(f'MSE: {mean_squared_error(y_true, y_pred)}')
    print(f'RMSE: {rmse}')
    r2 = r2_score(y_true, y_pred)
    print(f'r2: {r2}')
    print('_'*60)


    saved_defenders_df = epl_defenders_df[['Display_Name', 'First_Name','Last_Name','Player_Number', 'Position', 'Current_Club','So_5_Scores_9','sorare_xgb_predictions', 'sorare_lgbm_predictions', 'sorare_elastic_predictions', 'sorare_predictions']]
    saved_defenders_df.to_csv('sorare/sorare_data/predictions/sorare_defenders_predictions.csv', index=False)

    print('saved_defenders_df')