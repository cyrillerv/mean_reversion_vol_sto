import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pandas as pd
from src.mean_reversion import generate_signals

def test_generate_signals_output():
    data = pd.DataFrame({
        "price": [100, 101, 99, 102, 98, 100, 101, 99],
        "returns": [0.01] * 8,
        "volatility": [0.02] * 8,
    })
    result = generate_signals(data.copy(), ma_window=3, k=1.0)
    assert "signal" in result.columns
    assert result["signal"].isin([-1, 0, 1]).all()
