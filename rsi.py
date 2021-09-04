# Imports
import sys
import websocket, json, numpy as np, time
from datetime import datetime
import pandas as pd

def get_rsi():

    # -----Helper Functions-----
    def to_date(timestamp):
        date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
        return date

    # --------WebSocket---------
    SOCKET = "wss://stream.binance.com:9443/ws/ethusdc@kline_1m"
    closes = []
    dates = []
    df_dict = {}

    def on_open(ws):
        print("opened connection")

    def on_close(ws):
        print("closed connection")

    def on_message(ws, message):
        global closes
        global dates
        json_message = json.loads(message)
        # pprint.pprint(json_message)

        # Naming variables
        candle = json_message["k"]
        is_candle_closed = candle["x"]
        timestamp = candle["T"]
        close = float(candle["c"])
        close = round(close, 2)
        print(f"Current price of ETHUSDC is {close}\n-----------------------------------\n")

        # Saving the closes and timestamps
        if is_candle_closed:
            print(f"Candle closed at {close}".format(close))
            closes.append(float(close))

            # Timestamp must be divided by 1000 to get an accurate year
            date = to_date(timestamp/1000)
            dates.append(date)
            print(f"Closes - {closes}")
            print(f"Datetimes - {dates}")

        # Create a Dataframe is there is > 0 datapoints
        if len(closes) > 0:
            create_df(closes, dates)

    #--------DataFrame--------
    def create_df(closes, dates):
        if eth_df is False:
            df_dict["Date"], df_dict["ETHUSDC"] = dates, closes
            eth_df = pd.DataFrame.from_dict(df_dict)
            eth_df.set_index(column="Date", infer_datetime_format=True, parse_dates=True)
        else:
            eth_df["Date"].append(dates[-1])
            eth_df["ETHUSDC"].append(closes[-1])

        return eth_df 

    ws = websocket.WebSocketApp(SOCKET, on_open=on_open, on_close=on_close, on_message=on_message)
    ws.run_forever()

    return eth_df