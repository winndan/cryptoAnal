from alpaca.data.historical import CryptoHistoricalDataClient
from alpaca.data.requests import CryptoBarsRequest
from alpaca.data.timeframe import TimeFrame
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize the client (no keys required)
crypto_client = CryptoHistoricalDataClient()

# Define request parameters for historical bar data
request_params = CryptoBarsRequest(
    symbol_or_symbols=["DOGE/USDT"],
    timeframe=TimeFrame.Day,
    start=pd.to_datetime("2022-02-09"),
    end=pd.to_datetime(datetime.now())  # Set end date to current date
)

# Fetch historical bars and convert to DataFrame
bars = crypto_client.get_crypto_bars(request_params)
df_bars = bars.df

# Print the first few rows of the DataFrame for inspection
row_count = len(df_bars)
print(row_count)
