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
import lstm_eth
import lstm_btc
import ichimoku
import rsi
from trading import PortfolioManager
from alpaca_trade_api.rest import REST


st.set_page_config(
     page_title="Crypototo Roboto",
     page_icon="🪄",
     layout="centered",
     initial_sidebar_state="collapsed",
)

# ! Trading Sidebar - Start 
# TODO: Change the below key to your own API key or Please follow the README file to export keys 

alpaca_api_key = os.getenv("APCA_API_KEY_ID")
alpaca_secret_key = os.getenv("APCA_API_SECRET_KEY")
request = requests.get("https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&from_currency=ETH&to_currency=USD&apikey=R298VOBAB51H5V8O").json()
eth_price = round(float(request['Realtime Currency Exchange Rate']['5. Exchange Rate']), 2)
api = REST(alpaca_api_key, alpaca_secret_key, api_version='v2')
manager = PortfolioManager()

with st.sidebar.form(key ='execution form'):
    title = st.title('💸 Execute Trade Now!')
    my_account = st.header("Equity: $"+api.get_account().equity)
    my_buying_power = st.subheader("Buying Power: $"+api.get_account().buying_power)
    divider = st.markdown("---")
    eth_icon = st.image("https://media.giphy.com/media/DdpmhAQpQZzwHSrQ3f/giphy.gif?cid=ecf05e477ppdd3d2qdsrijoe2u0mgeaw9y3pa95xigzoozkd&rid=giphy.gif&ct=s")
    eth_price = st.metric(label="Current Price in $USD", value = eth_price)
    eth_qty = st.number_input("Enter Quantity in ETH", value =0.10, min_value = 0.0, max_value = 10.0)    
    eth_side = st.selectbox("Do you wish to buy or sell?", ("buy", "sell"))
    submit = st.form_submit_button(label = 'Place Market Order Now ✅')

    if submit: 
        post_url = "https://paper-api.alpaca.markets/v2/orders"
        post_json = {"symbol":"TSLA", "qty":eth_qty, "side":eth_side, "type":"market", "time_in_force":"day"}
        post_header = {"APCA-API-KEY-ID":alpaca_api_key , "APCA-API-SECRET-KEY":alpaca_secret_key}
        response = requests.post(post_url, json = post_json, headers= post_header)

# ! Trading Sidebar - End

st.markdown(
"""
<style>
.wrapper {
  height: 5vh;
  /*This part is important for centering*/
  display: flex;
  align-items: center;
  justify-content: center;
}
.typing-demo {
  width: 22ch;
  animation: typing 2s steps(22), blink 0.5s step-end infinite alternate;
  white-space: nowrap;
  overflow: hidden;
  border-right: 3px solid;
  font-family: monospace;
  font-weight: bold;
  font-size: 4em;
}
@keyframes typing {
  from {
    width: 0;
  }
}
@keyframes blink {
  50% {
    border-color: transparent;
  }
}
</style>
<div class="wrapper">
    <div class="typing-demo">
      🪄 Crypototo Roboto
    </div>
</div>
<br />
<br />
<a href="https://github.com/cleopatrick1/Project_2"><img src="https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white" alt="github repo"></a>
<br />
<br />
<b>A one-stop shop of all the key trading signals and technical indicators! 🛍</b>
<br />
Don't forget to check out the <code>sidebar</code> where you can send order to Alpaca instantly without needed to switch between browser tabs! 
"""
, unsafe_allow_html=True)

"""
---
# 🎏 Ichimoku Cloud Trading Strategy
[Ichimoku cloud](https://www.investopedia.com/terms/i/ichimoku-cloud.asp) is designed to spot direction and momentum in order to help you make buy and sell decisions more easily.
\n Five indicators are used with each corresponding to a different timeline.
"""
st.write(ichimoku.get_ichimoku_plot())


"""
---
# 👀 Watch Out for Whales! 
Crypto market is not yet mature. Large players such as hedge funds and investment funds can use their advantage to manipulate the crypto price to their desired price to some extent, so it is important to always keep track of whale's movement and trade wisely!
\n Price available in $USD - credit: [@whale-alert](https://whale-alert.io)
"""

response = requests.get('https://api.whale-alert.io/v1/transactions?api_key=zd1tXydtCfegKwzLvUIMPCAasDBMiCnk&currency=eth&limit=5').json()
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
# 📈 Price Prediction with LSTM Machine Learning
[Long short-term memory (LSTM)](https://en.wikipedia.org/wiki/Long_short-term_memory) deep learning algorithm is a specialized architecture that can "memorize" patterns from historical sequences of data and extrapolate such patterns for future events. 
\n Here we try to use LSTM to predict ETH's closing price of the next trading day.
"""
st.write(lstm_eth.get_lstm_plot_data())
st.markdown("**However, it is fair more accurate when it comes to BTC!** ")
st.write(lstm_btc.get_lstm_plot_data())


"""
---
# 💹 RSI Trading Strategy
[RSI stands for Relative Strength Index](https://www.investopedia.com/terms/r/rsi.asp). It is a popular indicator for trading. When an assets RSI is below 30 it is considered oversold and a buy signal. When an assets RSI is above 70 it is considered overbought and a sell signal.
\n Below you will see a price feed for ETHUSD and the current RSI, when it is either overbought or oversold a signal will appear.
"""

chart_container = st.container()
price_container = st.container()
with chart_container:
    rsi.plot_chart()

with price_container:
    rsi.get_rsi_price()
