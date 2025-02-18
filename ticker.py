import yfinance as yf
import pandas as pd
import time

# 使用 wiki 選取 S&P500 成分股
sp500 = pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
sp500 = sp500[0]
tickers = sp500["Symbol"].tolist()

# 用 yf 爬 ROA 與 P/E ratio
fundamentals = {}

for ticker in tickers:  # 測試先爬前 50 檔，避免速度太慢
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        trailing_pe = info.get("trailingPE", None)
        forward_pe = info.get("forwardPE", None)
        roa = info.get("returnOnAssets", None)  # Yahoo Finance 的 ROA 是小數（如 0.12 表示 12%）

        fundamentals[ticker] = {"trailingPE": trailing_pe, "forwardPE": forward_pe, "ROA": roa * 100 if roa else None}
    except Exception as e:
        print(f"無法獲取 {ticker} 的資料: {e}")

    time.sleep(1)  # 避免請求過快被封鎖

fund_df = pd.DataFrame(fundamentals).T
print(fund_df.head())

pe_avg = fund_df["forwardPE"].dropna().mean()
roa_avg = fund_df["ROA"].dropna().mean()

# filtered_stocks = fund_df[(fund_df["PE"] < pe_avg) & (fund_df["ROA"] > roa_avg)]
filtered_stocks = fund_df[(fund_df["forwardPE"] < 15) & (fund_df["ROA"] > 10)]
filtered_tickers = filtered_stocks.index.tolist()
print(f"篩選後的股票：{filtered_tickers}")