from prophet import Prophet

def train_prophet(df):
    temp = df[['date', 'total']].rename(columns={'date': 'ds', 'total': 'y'})
    model = Prophet()
    model.fit(temp)
    return model

def forecast_prophet(model, periods):
    future = model.make_future_dataframe(periods=periods, freq='W')
    forecast = model.predict(future)
    return forecast[['ds', 'yhat']].tail(periods)