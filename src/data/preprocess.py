import pandas as pd

def preprocess(df):
    # Convert date column
    df['date'] = pd.to_datetime(df['date'])

    # Clean total column (remove brackets, commas)
    df['total'] = df['total'].astype(str)
    df['total'] = df['total'].str.replace('[(),]', '', regex=True)
    df['total'] = df['total'].astype(float)

    # Sort values
    df = df.sort_values(['state', 'date'])

    return df