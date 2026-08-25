
import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    .stApp{
      background:
      radial-gradient(circle at 5% 5%,rgba(69,110,255,.24),transparent 25%),
      radial-gradient(circle at 95% 5%,rgba(190,70,255,.20),transparent 25%),
      radial-gradient(circle at 75% 90%,rgba(0,210,190,.13),transparent 28%),
      linear-gradient(135deg,#050711,#091126 50%,#080613);
      color:#f5f7ff;
    }
    section[data-testid="stSidebar"]{
      background:linear-gradient(180deg,#090d1b,#050711);
      border-right:1px solid rgba(255,255,255,.08)
    }
    .hero,.feature,.news,.chatbox,.metric{
      border:1px solid rgba(255,255,255,.09);
      border-radius:22px;
      background:linear-gradient(135deg,rgba(20,29,57,.88),rgba(9,13,28,.88));
      box-shadow:0 18px 60px rgba(0,0,0,.25)
    }
    .hero{padding:35px;margin-bottom:25px}
    .hero h1{font-size:43px}
    .feature{padding:25px;margin-bottom:15px}
    .eyebrow{font-size:11px;letter-spacing:1.7px;color:#91a0c2;font-weight:800}
    .big{font-size:39px;font-weight:900;margin:10px 0}
    .pill{display:inline-block;padding:8px 13px;border-radius:999px;
          background:rgba(110,135,255,.18);border:1px solid rgba(140,160,255,.25)}
    .metric{padding:19px}
    .label{font-size:11px;color:#8e9ab7;letter-spacing:1px}
    .value{font-size:24px;font-weight:850;margin-top:6px}
    .sub{font-size:12px;color:#8390a9;margin-top:5px}
    .news{padding:17px;margin:10px 0}
    .news a{color:#aebfff}
    .chatbox{padding:18px;margin-bottom:14px}
    .stButton>button{border-radius:12px;font-weight:700}
    #MainMenu,footer{visibility:hidden}
    </style>
    """,unsafe_allow_html=True)

def metric_card(title,value,subtitle):
    st.markdown(f"""<div class="metric">
    <div class="label">{title}</div><div class="value">{value}</div>
    <div class="sub">{subtitle}</div></div>""",unsafe_allow_html=True)

def section_title(title):
    st.markdown(f"### {title}")

def hero(ticker):
    st.markdown(f"""<div class="hero">
    <h1>📈 StockPredict AI <span style="opacity:.4">PRO</span></h1>
    <div style="color:#aeb9d0">Advanced ML forecasting · Technical intelligence · News sentiment · AI assistant</div>
    <br><b>Analyzing:</b> {ticker}</div>""",unsafe_allow_html=True)
