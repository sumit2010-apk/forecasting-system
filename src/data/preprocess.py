import pandas as pd

def preprocess(df):
    
    df['date'] = pd.to_datetime(df['date'])

    
    df['total'] = df['total'].astype(str)
    df['total'] = df['total'].str.replace('[(),]', '', regex=True)
    df['total'] = df['total'].astype(float)

    
    df = df.sort_values(['state', 'date'])

    return df
