def create_features(df):
    df = df.copy()
    df = df.set_index('date')

    
    df['lag1'] = df['total'].shift(1)
    df['lag7'] = df['total'].shift(7)
    df['lag30'] = df['total'].shift(30)

    
    df['rolling_mean'] = df['total'].rolling(window=7).mean()
    df['rolling_std'] = df['total'].rolling(window=7).std()

    
    df['day_of_week'] = df.index.dayofweek
    df['month'] = df.index.month

    
    df = df.dropna()

    return df.reset_index()
