# Imports
import streamlit as st
import sys
import websocket, json, pprint, numpy as np, time, datetime
from datetime import datetime
import pandas as pd
import pytz, requests
import yfinance as yf
import plotly.graph_objs as go
import plotly.express as px

# Cufflinks
import cufflinks as cf
cf.set_config_file(theme='solar',sharing='public')

# Helper functions
def ticker_data(ticker, period, interval):
    data = yf.Ticker(ticker).history(period=period, interval=interval)
    return data

# Cufflinks Quantfig helper function
def create_quantfig(data, title, name):
    quantfig = cf.QuantFig(data, title=title,legend='top',name=name, up_color="green", down_color="red")
    quantfig.add_sma([10,20],width=2,color=['green','lightgreen'],legendgroup=True)
    quantfig.add_bollinger_bands(periods=20,boll_std=2,colors=['magenta','grey'],fill=True)
    quantfig.add_rsi(periods=20,color='java')
    
    return quantfig

# Plot chart function to be called in streamlit_app.py
def plot_chart():
    eth_df = ticker_data("ETH-USD", "2d", "1m")
    eth_df.reset_index(inplace=True)
    eth_df.set_index("Datetime", inplace=True)
    
    eth_candles = create_quantfig(eth_df, "ETH-USD, 1m", "ETH")

    fig = eth_candles.iplot(asFigure=True, title="ETH-USD, 1m")
    fig.update_layout(height=500, width=750, title_text="ETH-USD Chart 1m")

    st.plotly_chart(fig)

# AEDT to EDT function used for accessing latest RSI from API
# because the API json comes in EDT time
def aedt_to_edt():
    default_time = datetime.now()
    edt_info = pytz.timezone("US/Eastern")
    edt_time = default_time.astimezone(edt_info).strftime("%Y-%m-%d %H:%M")
    return edt_time

# Get latest rsi calls aedt_to_edt() and then accesses the latest RSI from the API json
def get_latest_rsi():
    # Spare API keys
    # url = 'https://www.alphavantage.co/query?function=RSI&symbol=ETHUSD&interval=1min&time_period=14&series_type=close&apikey=HQ2OSP15VI0XOKJD'
    # url = 'https://www.alphavantage.co/query?function=RSI&symbol=ETHUSD&interval=1min&time_period=14&series_type=close&apikey=R298VOBAB51H5V8O'
    url = 'https://www.alphavantage.co/query?function=RSI&symbol=ETHUSD&interval=1min&time_period=14&series_type=close&apikey=HOSE4TMKXX8YTETD'
    r = requests.get(url)
    data = r.json()
    time = aedt_to_edt()
    rsi = data["Technical Analysis: RSI"][time]
    return float(rsi["RSI"])

# Gets called in streamlit_app.py and displays current ETHUSD price feed and current 1m RSI
def get_rsi_price():
# --------WebSocket---------
    # st.empties for price feed
    placeholder_price = st.empty()
    placeholder_rsi = st.empty()
    placeholder_rsi_sell = st.empty()
    placeholder_rsi_buy = st.empty()

    SOCKET = "wss://stream.binance.com:9443/ws/ethusdc@kline_1m"
    closes = []
    dates = []
    rsi = []


    RSI_PERIOD = 14
    RSI_OVERBOUGHT =  70
    RSI_OVERSOLD = 30
    TRADE_SYMBOL = "ETHUSD"
    TRADE_QUANTITY = 0.1

    def on_open(wsapp):
        print("opened connection")

    def on_close(wsapp):
        print("closed connection")

    def on_message(wsapp, message):
        json_message = json.loads(message)

        # Naming variables
        candle = json_message["k"]
        is_candle_closed = candle["x"]
        timestamp = candle["T"]
        close = float(candle["c"])
        close = round(close, 2)
        if len(closes) >= 3:
            placeholder_price.subheader(f"Second last price of ETHUSDC is {closes[-2]}\nLast price of ETHUSDC is {closes[-1]}\nCurrent price of ETHUSDC is {close}")
        else: 
            placeholder_price.subheader(f"Current price of ETHUSDC is {close}")
        # RSI
        rsi.append(get_latest_rsi())
        placeholder_rsi.subheader(f"The current RSI is {rsi[-1]}")

        # Signals
        if rsi[-1] > RSI_OVERBOUGHT:
            placeholder_rsi_sell.subheader(f"The current RSI is {rsi[-1]}, this is a SELL signal")
        elif rsi[-1] < RSI_OVERSOLD:
            placeholder_rsi_buy.subheader(f"The current RSI is {rsi[-1]}, this is a BUY signal")

    wsapp = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    wsapp.run_forever()



