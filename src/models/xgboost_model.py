from xgboost import XGBRegressor
import pandas as pd
def forecast_xgb(model, df, steps=8):
    df = df.copy()
    df = df.set_index('date')

    predictions = []

    for _ in range(steps):
        # Create features
        df['lag1'] = df['total'].shift(1)
        df['lag7'] = df['total'].shift(7)
        df['lag30'] = df['total'].shift(30)

        df['rolling_mean'] = df['total'].rolling(7).mean()
        df['rolling_std'] = df['total'].rolling(7).std()

        df['day_of_week'] = df.index.dayofweek
        df['month'] = df.index.month

        df_feat = df.dropna().copy()

        # Take last row as input
        last_row = df_feat.iloc[-1:]

        X = last_row.drop(columns=['total', 'state', 'category'], errors='ignore')

        # Predict
        pred = model.predict(X)[0]
        predictions.append(pred)

        # Add new predicted row
        new_date = df.index[-1] + pd.Timedelta(weeks=1)

        new_row = pd.DataFrame({
            'date': [new_date],
            'total': [pred],
            'state': [df_feat.iloc[-1]['state']]
        }).set_index('date')

        df = pd.concat([df, new_row])

    return predictions
def train_xgb(X, y):
    model = XGBRegressor(n_estimators=100)
    model.fit(X, y)
    return model

def predict_xgb(model, X):
    return model.predict(X)