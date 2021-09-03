from collections import namedtuple
from pandas._libs.tslibs import timestamps
import altair as alt
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


st.set_page_config(
     page_title="Signals",
     page_icon="💎",
     layout="wide",
     initial_sidebar_state="auto",
)

"""
# Welcome to Streamlit!
Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:
If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).
In the meantime, below is an example of what you can do with just a few lines of code:
"""

"""
# 👀 Watchout for Whales!  
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
# 📈 Bitcoin Prediction with LSTM Machine Learning
Using the last 10 days trained data to predict next day price.
"""
st.write(lstm.get_lstm_plot_data())

