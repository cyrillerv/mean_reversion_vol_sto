def backtest_strategy(data):
    data["position"] = data["signal"].shift(1)
    data["strategy_returns"] = data["returns"] * data["position"]
    data["cumulative_returns"] = (1 + data["strategy_returns"]).cumprod()
    return data


if __name__ == "__main__":
    from data_loader import load_data
    from vol_model import estimate_volatility
    from mean_reversion import generate_signals
    data = load_data()
    data = estimate_volatility(data)
    data = generate_signals(data)
    df = backtest_strategy(data)
    print(df.head())