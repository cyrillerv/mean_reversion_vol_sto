def generate_signals(data, ma_window=20, k=1.0):
    data["ma"] = data["price"].rolling(ma_window).mean()
    data["signal"] = 0

    # Signal = 1 si prix bas, -1 si haut, 0 sinon
    buy_condition = data["price"] < data["ma"] - k * data["volatility"]
    sell_condition = data["price"] > data["ma"] + k * data["volatility"]

    data.loc[buy_condition, "signal"] = 1
    data.loc[sell_condition, "signal"] = -1
    return data.dropna()


if __name__ == "__main__":
    from data_loader import load_data
    from vol_model import estimate_volatility
    data = load_data()
    data = estimate_volatility(data)
    df = generate_signals(data)
    print(df.head())