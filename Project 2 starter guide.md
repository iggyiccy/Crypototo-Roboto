Hi and Welcome to Project 2
Project 2 is an open-source project which is developing a trading bot for every individual who is interested in crypto.
We are here to show you how to use pseudo code to get started with our bot.

Disclaimer: Our trading bot should consider as entertainment only, it is not any financial advice. Use this wisely.

# Import libraries and dependencies
import numpy as np
import pandas as pd
import hvplot.pandas
from pathlib import Path
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import os
import ccxt
import asyncio

import warnings
warnings.filterwarnings('ignore')

# read all csv and api as needed
your code here

# *Generate a Dual Moving Average Crossover Trading Signal to _short_ the market*
# Grab just the `date` and `close` from the IEX dataset
your code here

# Set the `date` column as the index
your code here

# Set the short window and long windows
your code here

# Generate the short and long moving averages (50 and 100 days, respectively)
your code here

# Initialize the new `Signal` column
your code here

# Generate the trading signal (1 or 0) to when the short window is less than the long
# Note: Use 1 when the SMA50 is less than SMA100 and 0 for when it is not.
your code here


# Calculate the points in time at which a position should be taken, 1 or -1
your code here


# Print the DataFrame
your code here

### Now, let's make this pretty by plotting it
# Plot Entry and Exit Points of Dual Moving Average Crossover Trading Strategy

your code here
# Visualize exit position relative to close price

# Visualize entry position relative to close price

# Visualize close price for the investment


# Visualize moving averages


# Overlay plots

### Now we will use the file jarvis.py to run the bot
