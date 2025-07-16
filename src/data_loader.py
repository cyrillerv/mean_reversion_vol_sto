import yfinance as yf
import pandas as pd

from pathlib import Path

def load_data(ticker="SPY", start="2015-01-01", end="2025-01-01", use_cache=True):
    path = Path(f"{ticker}_cache.csv")
    if path.exists() and use_cache:
        data = pd.read_csv(path)
        data.set_index("Date", inplace=True)
    else :
        data = yf.download(ticker, start=start, end=end)
        data = data["Close"][ticker].dropna().to_frame()
        data.rename(columns={ticker: "price"}, inplace=True)
        data["returns"] = data["price"].pct_change()
        data.dropna(inplace=True)
        data.to_csv(path)
    return data

if __name__ == "__main__":
    df = load_data()
    print(df.head())