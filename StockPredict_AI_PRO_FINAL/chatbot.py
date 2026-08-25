
def answer_question(question,ticker,current_price,predicted_price,predicted_return,
                    signal,rsi,ma20,ma50,volatility,language="English"):
    q = str(question).strip().lower()
    if not q:
        return "Please ask a stock-related question."

    if any(x in q for x in ["current price","current rate","stock price","price now",
                             "price today","latest price","rate"]):
        ans = f"{ticker} is currently around ${current_price:,.2f} based on loaded market data."
    elif "rsi" in q or "overbought" in q or "oversold" in q:
        zone = "overbought" if rsi >= 70 else "oversold" if rsi <= 30 else "neutral"
        ans = f"{ticker} RSI is {rsi:.2f}, currently in the {zone} zone."
    elif any(x in q for x in ["predict","prediction","forecast","tomorrow","next day","expected price"]):
        ans = (f"{ticker} is around ${current_price:,.2f}. The model estimates "
               f"${predicted_price:,.2f} for the next trading day, with estimated "
               f"return {predicted_return:+.2f}%. Signal: {signal}.")
    elif any(x in q for x in ["technical","indicator","analysis"]):
        ans = (f"Technical snapshot for {ticker}: price ${current_price:,.2f}, "
               f"MA20 ${ma20:,.2f}, MA50 ${ma50:,.2f}, RSI {rsi:.2f}, "
               f"volatility {volatility:.2f}%, signal {signal}.")
    elif "ma20" in q or "20 day" in q:
        ans = f"{ticker} MA20 is ${ma20:,.2f}; current price is ${current_price:,.2f}."
    elif "ma50" in q or "50 day" in q:
        ans = f"{ticker} MA50 is ${ma50:,.2f}; current price is ${current_price:,.2f}."
    elif "volatility" in q:
        level = "high" if volatility > 4 else "moderate" if volatility > 2 else "relatively low"
        ans = f"{ticker} volatility is {volatility:.2f}%, indicating {level} short-term movement."
    elif "risk" in q:
        level = "high" if volatility > 4 else "moderate" if volatility > 2 else "relatively low"
        ans = f"{ticker} shows {level} short-term risk based on volatility of {volatility:.2f}%."
    elif any(x in q for x in ["signal","recommendation","buy","sell","should i"]):
        ans = (f"The model signal for {ticker} is {signal}; estimated next-day return is "
               f"{predicted_return:+.2f}%. This is an educational model output, not financial advice.")
    elif any(x in q for x in ["overview","complete","everything","about"]):
        ans = (f"{ticker}: price ${current_price:,.2f}, prediction ${predicted_price:,.2f}, "
               f"return {predicted_return:+.2f}%, RSI {rsi:.2f}, MA20 ${ma20:,.2f}, "
               f"MA50 ${ma50:,.2f}, volatility {volatility:.2f}%, signal {signal}.")
    else:
        ans = ("I can answer questions about current price, prediction, RSI, technical "
               "analysis, MA20, MA50, volatility, risk and AI signal.")
    if language != "English":
        ans += f"\n\n🌐 Selected language: {language}."
    return ans
