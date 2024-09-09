import pandas as pd

import numpy as np

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder

from sorare.utils_data_structures import col_prefixes



def scale_columns(df, scaler, scaling_columns):
    return scaler.fit_transform(df[scaling_columns])

def scale_sorare5_scores(df):
    # scale So_5_Scores and Avg Price
    # scaling with numpy since data distribution is highly skewed - can handle zeros
    columns_to_transform = _get_transform_columns()
    df[columns_to_transform] = np.log1p(df[columns_to_transform])  # log1p is log(1 + x) which handles zeros

    df['Has_Issue_Bool'] = df['Active_Injuries_Bool'] | df['Active_Suspensions_Bool']
    df = df.drop(columns=['Display_Name',	'First_Name','Last_Name', 'Player_Number', 'Active_Injuries_Bool', 'Active_Suspensions_Bool'])



# internal function
def _get_transform_columns():
    columns_to_transform = []
    for col in col_prefixes:
        for index in range(0, 10):
            columns_to_transform.append(f'{col}_{index}')
    return columns_to_transform


col_prefixes = [
    'So_5_Scores',
    'accuratePass',
    'assistPenaltyWon',
    'bigChanceCreated',
    'cleanSheet',
    'cleanSheet60',
    'crossAccuracy',
    'duelWon',
    'effectiveClearance',
    'errorLeadToGoal',
    'fouls',
    'gameStarted',
    'goalAssist',
    'goals',
    'interceptionWon',
    'lastManTackle',
    'minsPlayed',
    'ownGoals',
    'passAccuracy',
    'penaltiesSaved',
    'penaltyConceded',
    'penaltyKickMissed',
    'penaltySave',
    'redCard',
    'saves',
    'shotAccuracy',
    'totalClearance',
    'totalPass',
    'wonTackle',
    'yellowCard'
]