import yfinance as yf
import pandas as pd

def load_data(ticker="SPY", start="2015-01-01", end="2025-01-01"):
    data = yf.download(ticker, start=start, end=end)
    data = data["Close"][ticker].dropna().to_frame()
    data.rename(columns={ticker: "price"}, inplace=True)
    data["returns"] = data["price"].pct_change()
    return data.dropna()

if __name__ == "__main__":
    df = load_data()
    print(df.head())