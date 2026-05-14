import pandas as pd

df = pd.read_csv('data_cleaned.csv')

districts  = sorted(df['district'].unique().tolist())
fort_types = sorted(df['type'].unique().tolist())
difficulties = ['Easy', 'Medium', 'Hard']
seasons    = sorted(df['best_season'].unique().tolist())
conditions = sorted(df['current_condition'].unique().tolist())