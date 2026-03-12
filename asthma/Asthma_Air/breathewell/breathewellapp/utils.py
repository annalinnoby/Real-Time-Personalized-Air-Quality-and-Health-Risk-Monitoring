from statsmodels.tsa.arima.model import ARIMA

def arima_forecast(series, steps=10):
    series = series.astype(float)  # 🔥 force float
    model = ARIMA(series, order=(2, 1, 2))
    model_fit = model.fit()
    return model_fit.forecast(steps=steps)
