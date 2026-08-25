
from pathlib import Path
import pandas as pd

try:
    import yfinance as yf
except Exception:
    yf = None

BASE = Path(__file__).resolve().parent
CSV = BASE / "data" / "stock_data.csv"

ALIASES = {
    "apple":"AAPL","microsoft":"MSFT","google":"GOOGL","alphabet":"GOOGL",
    "amazon":"AMZN","tesla":"TSLA","nvidia":"NVDA","meta":"META","netflix":"NFLX",
    "reliance":"RELIANCE.NS","reliance industries":"RELIANCE.NS",
    "tcs":"TCS.NS","infosys":"INFY.NS","hdfc":"HDFCBANK.NS",
    "icici":"ICICIBANK.NS","sbi":"SBIN.NS","wipro":"WIPRO.NS","itc":"ITC.NS"
}

def resolve_ticker(value):
    q = str(value or "").strip().lower()
    if not q:
        return None
    if q in ALIASES:
        return ALIASES[q]
    symbol = q.upper().replace(" ","")
    indian = {"RELIANCE","TCS","INFY","HDFCBANK","ICICIBANK","SBIN","WIPRO","ITC"}
    if symbol in indian:
        return symbol + ".NS"
    return symbol

def normalize(df):
    if df is None or df.empty:
        return pd.DataFrame()
    out = df.copy()
    if isinstance(out.columns, pd.MultiIndex):
        out.columns = [x[0] if isinstance(x, tuple) else x for x in out.columns]
    mapping = {"date":"Date","open":"Open","high":"High","low":"Low",
               "close":"Close","adj close":"Adj Close","volume":"Volume",
               "ticker":"Ticker","symbol":"Ticker"}
    out.rename(columns={c:mapping.get(str(c).strip().lower(),c) for c in out.columns},
               inplace=True)
    if "Date" in out.columns:
        out["Date"] = pd.to_datetime(out["Date"], errors="coerce")
        out = out.set_index("Date")
    return out

def load_local(ticker):
    if not CSV.exists():
        return pd.DataFrame()
    try:
        df = normalize(pd.read_csv(CSV))
        if "Ticker" in df:
            df = df[df["Ticker"].astype(str).str.upper() == ticker.upper()]
        if {"Open","High","Low","Close","Volume"}.issubset(df.columns):
            return df.sort_index()
    except Exception:
        pass
    return pd.DataFrame()

def get_market_data(ticker, period="2y"):
    ticker = resolve_ticker(ticker)
    if not ticker:
        return pd.DataFrame()
    if yf:
        try:
            df = normalize(yf.download(ticker, period=period, interval="1d",
                                        auto_adjust=False, progress=False,
                                        threads=False))
            if {"Open","High","Low","Close","Volume"}.issubset(df.columns):
                return df.dropna(subset=["Close"])
        except Exception:
            pass
    return load_local(ticker)

def get_stock_news(ticker):
    if not yf:
        return []
    try:
        raw = yf.Ticker(resolve_ticker(ticker)).news or []
    except Exception:
        return []
    result = []
    for item in raw[:8]:
        c = item.get("content") or {}
        title = c.get("title") or item.get("title") or "Market Update"
        provider = (c.get("provider") or {}).get("displayName") or item.get("publisher") or "Market News"
        url = (c.get("canonicalUrl") or {}).get("url") or item.get("link") or "#"
        result.append({"title":str(title),"provider":str(provider),"url":str(url)})
    return result
