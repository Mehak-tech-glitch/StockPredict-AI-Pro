
import numpy as np

try:
    from sklearn.ensemble import RandomForestRegressor
except Exception:
    RandomForestRegressor = None

FEATURES = ["Close","MA20","MA50","RSI","MACD","MACD_Signal","Returns"]

def predict_next_day(data):
    clean = data.dropna(subset=FEATURES).copy()
    if len(clean) < 40 or RandomForestRegressor is None:
        current = float(data["Close"].iloc[-1])
        recent = data["Close"].tail(5)
        ret = ((recent.iloc[-1]/recent.iloc[0])-1)*100 if len(recent) > 1 else 0
        predicted = current * (1 + ret/500)
        signal = "Bullish" if ret > .5 else "Bearish" if ret < -.5 else "Neutral"
        return {"predicted_price":predicted,"predicted_return":(predicted/current-1)*100,
                "signal":signal,"confidence":55.0,"model_used":"Technical fallback"}

    X = clean[FEATURES].iloc[:-1].values
    y = clean["Close"].iloc[1:].values
    model = RandomForestRegressor(n_estimators=180, max_depth=10,
                                  random_state=42, n_jobs=-1)
    model.fit(X, y)
    predicted = float(model.predict(clean[FEATURES].iloc[-1:].values)[0])
    current = float(clean["Close"].iloc[-1])
    ret = (predicted/current-1)*100
    signal = "Bullish" if ret > .5 else "Bearish" if ret < -.5 else "Neutral"
    confidence = min(95.0, max(50.0, 60.0 + abs(ret)*5))
    return {"predicted_price":predicted,"predicted_return":ret,
            "signal":signal,"confidence":confidence,"model_used":"Random Forest"}
