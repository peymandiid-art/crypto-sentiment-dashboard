import streamlit as st
import requests
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Crypto Sentiment Dashboard", page_icon="📊", layout="wide")

st.title("📊 Crypto Market Sentiment Dashboard")
st.markdown("این داشبورد احساس بازار کریپتو را بر اساس شاخص ترس و طمع و داده‌های قیمت نمایش می‌دهد.")

# --- Fear & Greed Index ---
fg_url = "https://api.alternative.me/fng/?limit=7"
fg_data = requests.get(fg_url).json()
fg_df = pd.DataFrame(fg_data['data'])
fg_df['value'] = fg_df['value'].astype(int)
fg_df['timestamp'] = pd.to_datetime(fg_df['timestamp'], unit='s')

current_fear = fg_df.iloc[0]['value']
st.metric(label="📈 Current Fear & Greed Index", value=current_fear)

# Plot 7-day trend
fig_fg = px.line(fg_df, x='timestamp', y='value', title="Fear & Greed Index - Last 7 Days", markers=True)
st.plotly_chart(fig_fg, use_container_width=True)

# --- Crypto Prices ---
prices = requests.get("https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd").json()
col1, col2 = st.columns(2)
col1.metric("Bitcoin (BTC)", f"${prices['bitcoin']['usd']:,}")
col2.metric("Ethereum (ETH)", f"${prices['ethereum']['usd']:,}")

st.info("Data source: alternative.me & CoinGecko APIs")
