from data.load_data import load_data
from data.preprocess import preprocess
from utils.helpers import fill_missing_dates
from features.feature_engineering import create_features

from models.arima_model import train_arima, forecast_arima
from models.prophet_model import train_prophet, forecast_prophet
from models.xgboost_model import train_xgb, predict_xgb

from evaluation.evaluate import evaluate

import pandas as pd
import pickle

DATA_PATH = "data/raw/sales.xlsx"

df = load_data(DATA_PATH)
df = preprocess(df)
df = fill_missing_dates(df)

states = df['state'].unique()

results = {}

for state in states:
    print(f"\nProcessing State: {state}")

    temp = df[df['state'] == state].copy()

    # =========================
    # ARIMA
    # =========================
    series = temp.set_index('date')['total']

    arima_model = train_arima(series)

    train_size = int(len(series) * 0.8)
    train, test = series[:train_size], series[train_size:]

    arima_pred = arima_model.forecast(steps=len(test))
    arima_mae = evaluate(test, arima_pred)

    # =========================
    # PROPHET
    # =========================
    prophet_model = train_prophet(temp)

    prophet_forecast = forecast_prophet(prophet_model, len(test))
    prophet_pred = prophet_forecast['yhat'].values

    prophet_mae = evaluate(test.values, prophet_pred)

    # =========================
    # XGBOOST
    # =========================
    feat_df = create_features(temp)

    X = feat_df.drop(columns=['total', 'state', 'date', 'category'], errors='ignore')
    y = feat_df['total']

    split = int(len(X) * 0.8)
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    xgb_model = train_xgb(X_train, y_train)
    xgb_pred = predict_xgb(xgb_model, X_test)

    xgb_mae = evaluate(y_test, xgb_pred)

    # =========================
    # COMPARE MODELS
    # =========================
    scores = {
        "ARIMA": arima_mae,
        "PROPHET": prophet_mae,
        "XGBOOST": xgb_mae
    }

    best_model = min(scores, key=scores.get)

    print("MAE Scores:", scores)
    print("Best Model:", best_model)

    if best_model == "ARIMA":
     results[state] = arima_model
    elif best_model == "PROPHET":
     results[state] = prophet_model
    else:
     results[state] = xgb_model

print("\nFINAL RESULTS:")
print(results)
# Save best models
pickle.dump(results, open("models.pkl", "wb"))

print("\nModels saved successfully!")