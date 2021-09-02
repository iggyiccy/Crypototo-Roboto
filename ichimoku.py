import nest_asyncio
import os
import ccxt
import asyncio
import numpy as np
import pandas as pd
import plotly.express as px
import hvplot.pandas
from pathlib import Path
from pandas_datareader import data, wb
import yfinance as yf
import datetime as dt
import matplotlib.pyplot as plt
from chart_studio import plotly
from plotly.subplots import make_subplots
import plotly.graph_objs as go
from plotly.offline import init_notebook_mode, plot, iplot
import kaleido


# Range of Crypto

#def fetch_data():
ticker = ["ETH-USD"]

#start = pd.to_datetime('2020-01-01')
end = dt.datetime.now().date()
crypto_df = yf.download(ticker, period = "1y", group_by = 'ticker', threads = True, progress=False)[['Open','High','Low','Close']].dropna()
#return crypto_df
#fetch_data().tail()


index = pd.date_range(end, periods=26, freq='D')
columns = crypto_df.columns
dfna = pd.DataFrame(index=index, columns=columns)
crypto_df = pd.concat([crypto_df,dfna])

# Tenkan-sen (Conversion Line): (nine-period high + nine-period low)/2))
nine_period_high = crypto_df['High'].rolling(window= 9).max()
nine_period_low = crypto_df['Low'].rolling(window= 9).min()
crypto_df['tenkan_sen'] = (nine_period_high + nine_period_low) /2

# Kijun-sen (Base Line): (26-period high + 26-period low)/2))
period26_high = crypto_df['High'].rolling(window=26).max()
period26_low = crypto_df['Low'].rolling(window=26).min()
crypto_df['kijun_sen'] = (period26_high + period26_low) / 2

# The most current closing price plotted 26 time periods behind (optional)
crypto_df['chikou_span'] = crypto_df['Close'].shift(-26)

# Senkou Span A (Leading Span A): (Conversion Line + Base Line)/2))
crypto_df['senkou_span_a'] = ((crypto_df['tenkan_sen'] + crypto_df['kijun_sen']) / 2).shift(26)

# Senkou Span B (Leading Span B): (52-period high + 52-period low)/2))
period52_high = crypto_df['High'].rolling(window=52).max()
period52_low = crypto_df['Low'].rolling(window=52).min()
crypto_df['senkou_span_b'] = ((period52_high + period52_low) / 2).shift(26)

# Grab just the `date` and `close` from the IEX dataset
#ichimoku_signals_df = pd.DataFrame(crypto_df['Close'])
crypto_df.index.name = 'Date'

# Initialize the new `Signal1` column
crypto_df['Signal1'] = 0

# Generate the trading signal (1 or 0) to when the -----Conversion cross over the Base-----
# Note: Use 1 when Conversion is more than/crosses over the Base and 0 for when it is not/lower.
#Conversion
crypto_df['Signal1'] = np.where(
    (crypto_df['tenkan_sen'].shift(1) <= crypto_df['kijun_sen'].shift(1)) & (crypto_df['tenkan_sen'] > crypto_df['kijun_sen']), 1, crypto_df['Signal1'])
#Base
crypto_df['Signal1'] = np.where(
    (crypto_df['tenkan_sen'].shift(1) >= crypto_df['kijun_sen'].shift(1)) & (crypto_df['tenkan_sen'] < crypto_df['kijun_sen']), -1, crypto_df['Signal1'])


df_new = crypto_df[crypto_df['Signal1'] == 1.0][['Close']]

#declare figure

fig = go.Figure()

# Set up traces
fig.add_trace(go.Candlestick(x=crypto_df.index,
                            open=crypto_df['Open'],
                            high=crypto_df['High'],
                            low=crypto_df['Low'],
                            close=crypto_df['Close'], name = 'market data'))


fig.add_trace(go.Scatter(x=crypto_df.index, y= crypto_df['tenkan_sen'],line=dict(color='royalblue', width=.8), name = 'Conversion Line'))
fig.add_trace(go.Scatter(x=crypto_df.index, y= crypto_df['kijun_sen'],line=dict(color='darkorange', width=.8), name = 'Base Line'))
fig.add_trace(go.Scatter(x=crypto_df.index, y= crypto_df['senkou_span_a'],line=dict(color='green', width=.8), name = 'Leading A'))
fig.add_trace(go.Scatter(x=crypto_df.index, y= crypto_df['senkou_span_b'],line=dict(color='red', width=.8), name = 'Leading B'))
fig.add_trace(go.Scatter(x=crypto_df.index, y= crypto_df['chikou_span'],line=dict(color='black', width=.8), name = 'Lagging Span'))

# Visualize entry position relative to close price
fig.add_trace(go.Scatter(x= df_new.index, 
                         y= df_new['Close'],
                         marker_color='yellow', 
                         mode="markers", 
                         name = 'Entry', 
                         marker=dict(showscale=True)))


#Show
fig.update_layout(height=900, width=1100, title_text="Entry and Exit Points of Ichimoku Span A & B crossover Trading Strategy")
fig.layout.plot_bgcolor = 'darkgrey'
print("----------------------Buy when green dot appears------------------------")
print("----------------------Sell when red dot appears------------------------")
fig.show()


//////////////////////////////////////////////////////////////////////////////////////////////////////////

def entry_exit_plot():
    # Visualize exit position relative to close price
    exit = crypto_df[crypto_df['Signal1'] == -1.0]['Close'].hvplot.scatter(
        color='red',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400)

# Visualize entry position relative to close price
    entry = crypto_df[crypto_df['Signal1'] == 1.0]['Close'].hvplot.scatter(
        color='green',
        legend=False,
        ylabel='Price in $',
        width=1000,
        height=400)

# Visualize close price for the investment
    security_close = crypto_df[['Close']].hvplot(
        line_color='lightgray',
        ylabel='Price in $',
        width=1000,
        height=400)

# Visualize moving averages
    conversionline = crypto_df[['tenkan_sen']].hvplot(
        color='green',
        ylabel='Price in $',
        width=1000,
        height=400)

    baseline = crypto_df[['kijun_sen']].hvplot(
        color='red',
        ylabel='Price in $',
        width=1000,
        height=400)

    print("----------------------Buy when green dot appears------------------------")
    print("----------------------Sell when red dot appears------------------------")
    entry_exit_plot = security_close * conversionline * baseline * entry * exit
    entry_exit_plot.opts(xaxis=None)
    return entry_exit_plot
entry_exit_plot()