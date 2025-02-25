import pandas as pd
import numpy as np
import yfinance as yf
import talib

# 下載歷史數據
ticker = "AAPL"
data = yf.download(tickers=ticker, start="2022-01-01", end="2024-01-01")

# 計算布林通道
data['Middle_Band'] = data['Close'].rolling(window=20).mean()
data['Std_Dev'] = data['Close'].rolling(window=20).std()
data['Upper_Band'] = data['Middle_Band'] + (2 * data['Std_Dev'])
data['Lower_Band'] = data['Middle_Band'] - (2 * data['Std_Dev'])
data['BB_Width'] = (data['Upper_Band'] - data['Lower_Band']) / data['Middle_Band']

# 計算 MACD
data['MACD'], data['Signal'], _ = talib.MACD(np.ravel(data['Close'].values), fastperiod=12, slowperiod=26, signalperiod=9)

# 計算 RSI
data['RSI'] = talib.RSI(np.ravel(data['Close'].values), timeperiod=14)

# 計算 KD (Stochastic)
data['K'], data['D'] = talib.STOCH(np.ravel(data['High'].values), np.ravel(data['Low'].values), np.ravel(data['Close'].values), fastk_period=14, slowk_period=3, slowd_period=3)

# 判斷市場類型
data['Trend_Market'] = (data['BB_Width'] > 0.05) & (abs(data['MACD']) > abs(data['Signal']))
data['Sideways_Market'] = ~data['Trend_Market']

# 交易策略：震盪市場
data['Buy_Signal'] = (data['Sideways_Market']) & (data['RSI'] < 30) & (data['K'] > data['D'])
data['Sell_Signal'] = (data['Sideways_Market']) & (data['RSI'] > 70) & (data['K'] < data['D'])

# 交易策略：趨勢市場
data['Trend_Buy'] = (data['Trend_Market']) & (data['MACD'] > data['Signal']) & (data['RSI'] > 50) & (data['K'] > data['D'])
data['Trend_Sell'] = (data['Trend_Market']) & (data['MACD'] < data['Signal']) & (data['RSI'] < 50) & (data['K'] < data['D'])

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
# import plotly.graph_objects as go
import numpy as np

# 繪製股價與布林通道
fig, ax = plt.subplots(3, 1, figsize=(14, 12), sharex=True)

# 1. 股價與布林通道
ax[0].plot(data.index, data['Close'], label="Close Price", color='blue', linewidth=1)
ax[0].plot(data.index, data['Upper_Band'], label="Upper Band", color='red', linestyle='--', linewidth=1)
ax[0].plot(data.index, data['Middle_Band'], label="Middle Band", color='green', linestyle='-', linewidth=1)
ax[0].plot(data.index, data['Lower_Band'], label="Lower Band", color='red', linestyle='--', linewidth=1)
ax[0].fill_between(data.index, data['Lower_Band'], data['Upper_Band'], color='gray', alpha=0.3)
ax[0].set_title(f"{ticker} Stock Price & Bollinger Bands")
ax[0].set_ylabel("Price")
ax[0].legend()

# 2. MACD 和 Signal Line
ax[1].plot(data.index, data['MACD'], label="MACD", color='blue', linewidth=1)
ax[1].plot(data.index, data['Signal'], label="Signal Line", color='red', linestyle='--', linewidth=1)
ax[1].bar(data.index, data['MACD'] - data['Signal'], label="MACD Histogram", color='green', alpha=0.3)
ax[1].set_title(f"{ticker} MACD & Signal Line")
ax[1].set_ylabel("Value")
ax[1].legend()

# 3. RSI
ax[2].plot(data.index, data['RSI'], label="RSI", color='purple', linewidth=1)
ax[2].axhline(30, color='green', linestyle='--', linewidth=1, label="30 - Oversold")
ax[2].axhline(70, color='red', linestyle='--', linewidth=1, label="70 - Overbought")
ax[2].set_title(f"{ticker} RSI")
ax[2].set_ylabel("RSI Value")
ax[2].legend()

# 格式設置
ax[2].set_xlabel("Date")
ax[2].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
ax[2].xaxis.set_major_locator(mdates.MonthLocator())
fig.autofmt_xdate()

plt.tight_layout()
plt.show()