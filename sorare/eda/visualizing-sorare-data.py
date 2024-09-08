import pandas as pd

from scipy import stats
import matplotlib.pyplot as plt

cleaned_df = pd.read_csv('sorare/sorare_data/cleaned_sorare_data.csv')

Q1 = cleaned_df['So_5_Average_Percent'].quantile(0.25)
Q3 = cleaned_df['So_5_Average_Percent'].quantile(0.75)
IQR = Q3 - Q1

# Define outliers as points that fall below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = cleaned_df[(cleaned_df['So_5_Average_Percent'] < lower_bound) | (cleaned_df['So_5_Average_Percent'] > upper_bound)]
print(len(outliers['So_5_Average_Percent']))
print(outliers['So_5_Average_Percent'])


cleaned_df['Z_Score'] = stats.zscore(cleaned_df['So_5_Average_Percent'])

# Define outliers as points with a Z-score greater than 3 or less than -3
outliers = cleaned_df[(cleaned_df['Z_Score'] > 2) | (cleaned_df['Z_Score'] < -2)]
print(len(outliers['Z_Score']))
print(outliers['Z_Score'])

plt.boxplot(cleaned_df['So_5_Average_Percent'])
plt.title('Boxplot of So_5_Average_Percent')
plt.show()

Q1 = cleaned_df['Average_Price'].quantile(0.25)
Q3 = cleaned_df['Average_Price'].quantile(0.75)
IQR = Q3 - Q1

# Define outliers as points that fall below Q1 - 1.5*IQR or above Q3 + 1.5*IQR
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = cleaned_df[(cleaned_df['Average_Price'] < lower_bound) | (cleaned_df['Average_Price'] > upper_bound)]
print(len(outliers['Average_Price']))
print(outliers['Average_Price'])

plt.boxplot(cleaned_df['Average_Price'])
plt.title('Boxplot of Average_Price')
plt.show()