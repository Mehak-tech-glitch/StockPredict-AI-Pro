
def add_indicators(df):
    out = df.copy()
    close = out["Close"]
    out["Returns"] = close.pct_change()
    out["MA20"] = close.rolling(20, min_periods=1).mean()
    out["MA50"] = close.rolling(50, min_periods=1).mean()

    delta = close.diff()
    gain = delta.clip(lower=0).rolling(14, min_periods=14).mean()
    loss = (-delta.clip(upper=0)).rolling(14, min_periods=14).mean()
    rs = gain / loss.replace(0, float("nan"))
    out["RSI"] = (100 - 100/(1+rs)).fillna(50)

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    out["MACD"] = ema12 - ema26
    out["MACD_Signal"] = out["MACD"].ewm(span=9, adjust=False).mean()
    return out
