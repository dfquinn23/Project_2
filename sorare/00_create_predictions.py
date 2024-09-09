# IM PROGRESS - FOR SOME REASON MY OUTPUT IS A BUNCH OF CLUBS

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error

from utils_models import load_models
from utils_data_structures import col_prefixes

epl_teams_ = pd.read_csv('sorare/sorare_data/large_cleaned_sorare_data.csv')

epl_teams_ = epl_teams_.fillna(0.0)

epl_teams_ = pd.get_dummies(epl_teams_, columns=['Current_Club'])

drop_columns = columns=['Display_Name', 'First_Name','Last_Name','Player_Number', 'Position']

goalkeepers_df = epl_teams_[epl_teams_['Position'] == 'Goalkeeper']
defenders_df = epl_teams_[epl_teams_['Position'] == 'Defender']
midfielders_df = epl_teams_[epl_teams_['Position'] == 'Midfielder']
forwards_df = epl_teams_[epl_teams_['Position'] == 'Forward']

goalkeepers_df = goalkeepers_df.drop(columns=drop_columns)
defenders_df = defenders_df.drop(columns=drop_columns)
midfielders_df = midfielders_df.drop(columns=drop_columns)
forwards_df = forwards_df.drop(columns=drop_columns)

# Create X and y and split into training and testing sets
target_column = 'So_5_Scores_9'
columns_to_drop = [f'{col}_9' for col in col_prefixes]

X_test_goalkeepers = goalkeepers_df.drop(columns=columns_to_drop)
y_test_goalkeepers = goalkeepers_df[target_column]

X_test_defenders = defenders_df.drop(columns=columns_to_drop)
y_test_defenders = defenders_df[target_column]

X_test_midfielders = midfielders_df.drop(columns=columns_to_drop)
y_test_midfielders = midfielders_df[target_column]

X_test_forwards = forwards_df.drop(columns=columns_to_drop)
y_test_forwards = forwards_df[target_column]

# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

models = load_models()
print(models)

y_test_goalkeepers['xgb_predictions'] = models['goalkeepers_xgb_model'].predict(X_test_goalkeepers)
y_test_goalkeepers['lgbm_predictions'] = models['goalkeepers_lgbm_model'].predict(X_test_goalkeepers)
y_test_goalkeepers['elastic_predictions'] = models['goalkeepers_elastic_model'].predict(X_test_goalkeepers)

y_test_defenders['xgb_predictions'] = models['defenders_xgb_model'].predict(X_test_defenders)
y_test_defenders['lgbm_predictions'] = models['defenders_lgbm_model'].predict(X_test_defenders)
y_test_defenders['elastic_predictions'] = models['defenders_elastic_model'].predict(X_test_defenders)

y_test_midfielders['xgb_predictions'] = models['midfielders_xgb_model'].predict(X_test_midfielders)
y_test_midfielders['lgbm_predictions'] = models['midfielders_lgbm_model'].predict(X_test_midfielders)
y_test_midfielders['elastic_predictions'] = models['midfielders_elastic_model'].predict(X_test_midfielders)

y_test_forwards['xgb_predictions'] = models['forwards_xgb_model'].predict(X_test_forwards)
y_test_forwards['lgbm_predictions'] = models['forwards_lgbm_model'].predict(X_test_forwards)
y_test_forwards['elastic_predictions'] = models['forwards_elastic_model'].predict(X_test_forwards)

print("y_test_df.head()")
