
import streamlit as st
import pandas as pd
from stock_utils import get_market_data, get_stock_news, resolve_ticker
from technical_indicators import add_indicators
from prediction_utils import predict_next_day
from chatbot import answer_question
from language_utils import LANGUAGES
from voice_utils import make_voice
from news_sentiment import analyze_news_sentiment
from ui import inject_css, metric_card, section_title, hero

st.set_page_config(page_title="StockPredict AI PRO", page_icon="📈", layout="wide")
inject_css()

if "ticker" not in st.session_state:
    st.session_state.ticker = "AAPL"
if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.markdown("## 📈 StockPredict AI")
    st.caption("Advanced ML Market Intelligence")

    query = st.text_input("🔎 Search stock", value=st.session_state.ticker,
                          placeholder="AAPL, MSFT, Reliance, TCS...")
    if st.button("Analyze Stock", use_container_width=True):
        symbol = resolve_ticker(query)
        if symbol:
            st.session_state.ticker = symbol
            st.session_state.messages = []
            st.rerun()
        else:
            st.error("Invalid stock symbol.")

    period_name = st.selectbox("Analysis period",
                               ["6 Months", "1 Year", "2 Years", "5 Years"],
                               index=2)
    period = {"6 Months":"6mo", "1 Year":"1y", "2 Years":"2y", "5 Years":"5y"}[period_name]

    st.divider()
    st.markdown("### ⭐ Popular")
    for symbol in ["AAPL","MSFT","GOOGL","AMZN","NVDA","TSLA","META",
                   "RELIANCE.NS","TCS.NS","INFY.NS","HDFCBANK.NS"]:
        if st.button(symbol, key="s_"+symbol, use_container_width=True):
            st.session_state.ticker = symbol
            st.session_state.messages = []
            st.rerun()

ticker = st.session_state.ticker

with st.spinner("Loading live market intelligence..."):
    data = get_market_data(ticker, period)

if data.empty:
    st.error("Market data unavailable. Check the ticker or internet connection.")
    st.stop()

data = add_indicators(data)
latest = data.iloc[-1]

current = float(latest["Close"])
previous = float(data["Close"].iloc[-2]) if len(data) > 1 else current
daily_change = (current / previous - 1) * 100 if previous else 0

prediction = predict_next_day(data)
predicted = prediction["predicted_price"]
predicted_return = prediction["predicted_return"]
signal = prediction["signal"]
confidence = prediction["confidence"]

rsi = float(latest["RSI"])
ma20 = float(latest["MA20"])
ma50 = float(latest["MA50"])
macd = float(latest["MACD"])
macd_signal = float(latest["MACD_Signal"])
volatility = float(data["Returns"].dropna().tail(30).std() * 100)

hero(ticker)

section_title("📊 Market Overview")
cols = st.columns(5)
values = [
    ("Current Price", f"${current:,.2f}", "Latest close"),
    ("Daily Change", f"{daily_change:+.2f}%", "vs previous close"),
    ("AI Forecast", f"${predicted:,.2f}", f"{predicted_return:+.2f}%"),
    ("Signal", signal, "ML direction"),
    ("Confidence", f"{confidence:.0f}%", "Model estimate"),
]
for col, (title, value, sub) in zip(cols, values):
    with col:
        metric_card(title, value, sub)

section_title("🧠 AI Prediction Engine")
a, b = st.columns([2,1])
with a:
    st.markdown(f"""
    <div class="feature">
    <div class="eyebrow">NEXT TRADING DAY FORECAST</div>
    <div class="big">{predicted:,.2f}</div>
    <div class="pill">{signal} · {predicted_return:+.2f}%</div>
    <p>Random Forest prediction using historical price and technical features.</p>
    </div>
    """, unsafe_allow_html=True)
with b:
    st.markdown(f"""
    <div class="feature">
    <div class="eyebrow">MODEL STATUS</div>
    <h3>Pipeline Ready ✓</h3>
    <p>✓ Market data</p><p>✓ Indicators</p><p>✓ ML forecast</p><p>✓ Risk analysis</p>
    <small>Confidence is not a guarantee.</small>
    </div>
    """, unsafe_allow_html=True)

section_title("📈 Price Chart")
try:
    import plotly.graph_objects as go
    chart = data.tail(260)
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=chart.index, open=chart["Open"],
                                 high=chart["High"], low=chart["Low"],
                                 close=chart["Close"], name="Price"))
    fig.add_trace(go.Scatter(x=chart.index, y=chart["MA20"], name="MA20"))
    fig.add_trace(go.Scatter(x=chart.index, y=chart["MA50"], name="MA50"))
    fig.update_layout(template="plotly_dark", height=540,
                      xaxis_rangeslider_visible=False,
                      paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig, use_container_width=True)
except Exception:
    st.line_chart(data["Close"].tail(260))

section_title("📡 Technical Intelligence")
cols = st.columns(5)
for col, title, value in zip(
    cols, ["RSI","MA20","MA50","MACD","Volatility"],
    [f"{rsi:.2f}",f"${ma20:,.2f}",f"${ma50:,.2f}",f"{macd:.2f}",f"{volatility:.2f}%"]
):
    with col:
        metric_card(title, value, "Calculated indicator")

section_title("📋 Recent Market Data")
st.dataframe(data.tail(15)[["Open","High","Low","Close","Volume"]].round(2),
             use_container_width=True)

section_title("📰 Market News")
news = get_stock_news(ticker)
if news:
    for item in news:
        sentiment = analyze_news_sentiment(item["title"])
        st.markdown(f"""
        <div class="news">
        <span class="eyebrow">{item["provider"]} · {sentiment}</span>
        <b>{item["title"]}</b><br>
        <a href="{item["url"]}" target="_blank">Read source →</a>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("No recent news returned by the data provider.")

section_title("🤖 AI Stock Enquiry Assistant")
st.markdown('<div class="chatbox"><b>Ask anything about the selected stock</b> · price · forecast · RSI · risk · technicals · signal</div>',
            unsafe_allow_html=True)

language = st.selectbox("🌐 Response language", LANGUAGES)

quick = st.columns(5)
quick_questions = [
    ("💰 Price","What is the current price?"),
    ("🔮 Forecast","What is the prediction?"),
    ("📊 Technicals","Give me technical analysis"),
    ("🛡️ Risk","What is the risk?"),
    ("🧠 Overview","Give me complete analysis"),
]
selected = None
for col, (label, question) in zip(quick, quick_questions):
    with col:
        if st.button(label, use_container_width=True):
            selected = question

question = st.chat_input(f"Ask about {ticker}...")
if selected:
    question = selected

if question:
    response = answer_question(question, ticker, current, predicted,
                                predicted_return, signal, rsi, ma20, ma50,
                                volatility, language)
    st.session_state.messages += [("user", question), ("assistant", response)]

for role, message in st.session_state.messages[-12:]:
    with st.chat_message(role):
        st.write(message)

if st.session_state.messages and st.session_state.messages[-1][0] == "assistant":
    if st.button("🔊 Voice Reply"):
        audio = make_voice(st.session_state.messages[-1][1], language)
        if audio:
            st.audio(audio)
        else:
            st.warning("Voice generation unavailable.")

st.caption("⚠️ Educational analytics only. ML predictions are estimates, not financial advice.")
