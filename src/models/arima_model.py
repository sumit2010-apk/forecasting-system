from statsmodels.tsa.arima.model import ARIMA

def train_arima(series):
    model = ARIMA(series, order=(5,1,0))
    return model.fit()

def forecast_arima(model, steps):
    return model.forecast(steps=steps)