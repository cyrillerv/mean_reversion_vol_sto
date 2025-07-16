from src.data_loader import load_data
from src.vol_model import estimate_volatility
from src.mean_reversion import generate_signals
from src.backtest import backtest_strategy
from src.plot_results import plot_results

from src.heston_model import heston_vol

def main():
    data = load_data()
    data = heston_vol(data)
    # data = estimate_volatility(data) # Simple rolling vol
    data = generate_signals(data)
    data = backtest_strategy(data)
    plot_results(data)

if __name__ == "__main__":
    main()
