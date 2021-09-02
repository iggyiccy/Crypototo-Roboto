import requests
import json
import time
import datetime
import pandas as pd

response = requests.get('https://api.whale-alert.io/v1/transactions?api_key=zd1tXydtCfegKwzLvUIMPCAasDBMiCnk&currency=btc').json()

whale_data = response["transactions"]

whale_df = pd.json_normalize(whale_data)

whale_df["timestamp"] = pd.to_datetime(whale_df["timestamp"], unit='s')

print(whale_df["timestamp"])