import pandas as pd
import numpy as np
import yfinance as yf
import talib

# 下載歷史數據
ticker = "AAPL"
data = yf.download(ticker, start="2022-01-01", end="2024-01-01")

# 計算布林通道
data['Middle_Band'] = data['Close'].rolling(window=20).mean()
data['Std_Dev'] = data['Close'].rolling(window=20).std()
data['Upper_Band'] = data['Middle_Band'] + (2 * data['Std_Dev'])
data['Lower_Band'] = data['Middle_Band'] - (2 * data['Std_Dev'])
data['BB_Width'] = (data['Upper_Band'] - data['Lower_Band']) / data['Middle_Band']

# 計算 MACD
data['MACD'], data['Signal'], _ = talib.MACD(data['Close'], fastperiod=12, slowperiod=26, signalperiod=9)

# 計算 RSI
data['RSI'] = talib.RSI(data['Close'], timeperiod=14)

# 計算 KD (Stochastic)
data['K'], data['D'] = talib.STOCH(data['High'], data['Low'], data['Close'], fastk_period=14, slowk_period=3, slowd_period=3)

# 判斷市場類型
data['Trend_Market'] = (data['BB_Width'] > 0.05) & (abs(data['MACD']) > abs(data['Signal']))
data['Sideways_Market'] = ~data['Trend_Market']

# 交易策略：震盪市場
data['Buy_Signal'] = (data['Sideways_Market']) & (data['RSI'] < 30) & (data['K'] > data['D'])
data['Sell_Signal'] = (data['Sideways_Market']) & (data['RSI'] > 70) & (data['K'] < data['D'])

# 交易策略：趨勢市場
data['Trend_Buy'] = (data['Trend_Market']) & (data['MACD'] > data['Signal']) & (data['RSI'] > 50) & (data['K'] > data['D'])
data['Trend_Sell'] = (data['Trend_Market']) & (data['MACD'] < data['Signal']) & (data['RSI'] < 50) & (data['K'] < data['D'])

# 顯示結果
print(data[['Close', 'BB_Width', 'MACD', 'Signal', 'RSI', 'K', 'D', 'Trend_Market', 'Sideways_Market', 'Buy_Signal', 'Sell_Signal', 'Trend_Buy', 'Trend_Sell']].tail(10))