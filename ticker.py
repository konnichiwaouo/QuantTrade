import yfinance as yf
import pandas as pd
import time

# 使用 wiki 選取 S&P500 成分股
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = sp500[0]
tickers = sp500["Symbol"].tolist()

# 用 yf 爬 ROA 與 P/E ratio
fundamentals = {}

for ticker in tickers[:50]:  # 測試先爬前 50 檔，避免速度太慢
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        pe_ratio = info.get("forwardPE", None)
        roa = info.get("returnOnAssets", None)  # Yahoo Finance 的 ROA 是小數（如 0.12 表示 12%）

        fundamentals[ticker] = {"PE": pe_ratio, "ROA": roa * 100 if roa else None}
    except Exception as e:
        print(f"無法獲取 {ticker} 的資料: {e}")

    time.sleep(1)  # 避免請求過快被封鎖

fund_df = pd.DataFrame(fundamentals).T
print(fund_df.head())