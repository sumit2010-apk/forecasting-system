from fastapi import FastAPI
import pickle
import pandas as pd
import traceback

# Import your modules
from src.models.xgboost_model import forecast_xgb
from src.data.load_data import load_data
from src.data.preprocess import preprocess
from src.utils.helpers import fill_missing_dates

app = FastAPI()

# Load trained models
models = pickle.load(open("models.pkl", "rb"))

# Dataset path
DATA_PATH = "data/raw/sales.xlsx"


@app.get("/")
def home():
    return {"message": "Forecasting API Running 🚀"}


@app.get("/forecast/{state}")
def forecast(state: str):
    state = state.capitalize()

    if state not in models:
        return {"error": "State not found"}

    model = models[state]

    # =========================
    # TRY ARIMA
    # =========================
    try:
        preds = model.forecast(steps=8)

        return {
            "state": state,
            "model_used": "ARIMA",
            "next_8_weeks_forecast": [float(x) for x in preds]
        }
    except:
        pass

    # =========================
    # TRY PROPHET
    # =========================
    try:
        future = model.make_future_dataframe(periods=8, freq='W')
        forecast = model.predict(future)

        preds = forecast['yhat'].tail(8).tolist()

        return {
            "state": state,
            "model_used": "PROPHET",
            "next_8_weeks_forecast": [float(x) for x in preds]
        }
    except:
        pass

    # =========================
    # TRY XGBOOST (REAL FORECAST)
    # =========================
    try:
        # Reload data
        df = load_data(DATA_PATH)
        df = preprocess(df)
        df = fill_missing_dates(df)

        # Filter state data
        state_df = df[df['state'] == state]

        preds = forecast_xgb(model, state_df, steps=8)

        return {
    "state": state,
    "model_used": "XGBOOST",
    "next_8_weeks_forecast": [float(x) for x in preds]
}
    except Exception as e:
     print("🔥 FULL ERROR:")
     traceback.print_exc()

     return {
        "error": str(e)
     }
    