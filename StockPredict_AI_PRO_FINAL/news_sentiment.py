
POS = {"beat","growth","surge","profit","strong","upgrade","gain","record","bullish","positive"}
NEG = {"loss","drop","fall","weak","downgrade","decline","bearish","negative","lawsuit","risk"}

def analyze_news_sentiment(text):
    words = set(str(text).lower().replace(","," ").replace("."," ").split())
    score = len(words & POS) - len(words & NEG)
    return "Positive" if score > 0 else "Negative" if score < 0 else "Neutral"
