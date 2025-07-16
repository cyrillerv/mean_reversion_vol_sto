import pandas as pd

# For now, we use a simple rolling volatility
def estimate_volatility(data, window=20):
    data["volatility"] = data["returns"].rolling(window).std()
    return data.dropna()

if __name__ == "__main__":
    from data_loader import load_data
    data = load_data()
    df = estimate_volatility(data)
    print(df.head())