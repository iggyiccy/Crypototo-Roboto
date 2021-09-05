from collections import namedtuple
from pandas._libs.tslibs import timestamps
import altair as alt
import os 
import math
import pandas as pd
import streamlit as st
import numpy as np
from bs4 import BeautifulSoup as BS
import requests
import urllib3
import time
import matplotlib.pyplot as plt
import plotly.express as px
import lstm
import ichimoku
from trading import PortfolioManager
from alpaca_trade_api.rest import REST
from PIL import Image

icon = Image.open("favicon.ico")
st.set_page_config(
     page_title="ProTrader",
     page_icon=icon,
     layout="centered",
     initial_sidebar_state="collapsed",
)

# ! Trading Sidebar - Start 
# TODO: Change the below key to your own API key or Make sure you have set your environment variables

alpaca_api_key = os.getenv("APCA_API_KEY_ID")
alpaca_secret_key = os.getenv("APCA_API_SECRET_KEY")
request = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=BTC&to_currency=USD&apikey=R298VOBAB51H5V8O").json()
btc_price = round(float(request['Realtime Currency Exchange Rate']['5. Exchange Rate']), 2)
api = REST(alpaca_api_key, alpaca_secret_key, api_version='v2')
manager = PortfolioManager()

with st.sidebar.form(key ='execution form'):
    title = st.title('💸 Execute Trade Now!')
    my_account = st.header("Equity: $"+api.get_account().equity)
    my_buying_power = st.subheader("Buying Power: $"+api.get_account().buying_power)
    divider = st.markdown("---")
    bitcoin_icon = st.image("bitcoin.gif")
    bitcoin_price = st.metric(label="Current Price in $USD", value = btc_price)
    bitcoin_qty = st.number_input("Enter Quantity in BTC", value =0.10, min_value = 0.0, max_value = 10.0)    
    bitcoin_side = st.selectbox("Do you wish to buy or sell bitcoin?", ("buy", "sell"))
    submit = st.form_submit_button(label = 'Place Market Order Now ✅')

    if submit: 
        post_url = "https://paper-api.alpaca.markets/v2/orders"
        post_json = {"symbol":"TSLA", "qty":bitcoin_qty, "side":bitcoin_side, "type":"market", "time_in_force":"day"}
        post_header = {"APCA-API-KEY-ID":alpaca_api_key , "APCA-API-SECRET-KEY":alpaca_secret_key}
        response = requests.post(post_url, json = post_json, headers= post_header)

# ! Trading Sidebar - End

"""
# Welcome to Streamlit!
Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).
In the meantime, below is an example of what you can do with just a few lines of code:
"""

"""
---
# 🎏 Ichimoku Cloud Trading Strategy
Ichimoku cloud is designed to spot direction and momentum in order to help you make buy and sell decisions more easily.
Five indicators are used with each corresponding to a different timeline.
"""
st.write(ichimoku.get_ichimoku_plot())


"""
---
# 👀 Watch Out for Whales!  
"""

response = requests.get('https://api.whale-alert.io/v1/transactions?api_key=zd1tXydtCfegKwzLvUIMPCAasDBMiCnk&currency=btc&limit=5').json()
whale_data = response["transactions"]
whale_df = pd.json_normalize(whale_data)
whale_df["timestamp"] = pd.to_datetime(whale_df["timestamp"], unit='s').dt.time
whale_df = whale_df[["timestamp", "amount_usd", "from.address", "from.owner"]]

cols = st.columns(5)
for whale in range(5):
    amount_usd = whale_df.iloc[whale, 1]
    timestamp = whale_df.iloc[whale, 0]
    cols[whale].metric(label=str(timestamp), value="🐋", delta=amount_usd)

"""
---
# 💹 RSI Trading Strategy

"""



"""
---
# 📈 Bitcoin Prediction with LSTM Machine Learning
Long short-term memory (LSTM) deep learning algorithm is a specialized architecture that can "memorize" patterns from historical sequences of data and extrapolate such patterns for future events. 
Here I try to use it to predict BTC's closing price of the next trading day.  
"""
st.write(lstm.get_lstm_plot_data())
