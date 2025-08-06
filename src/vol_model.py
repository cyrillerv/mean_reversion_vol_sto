import pandas as pd
import numpy as np
from arch import arch_model

def simple_vol(df_returns_input) :
    df_returns = df_returns_input.copy()
    return df_returns.rolling(window=25).std()

def calc_vol_garch(df_returns):
    df_vol = pd.DataFrame(index=df_returns.index)

    for col in df_returns.columns:
        model = arch_model(100 * df_returns[col], vol='Garch', p=1, q=1)
        res = model.fit(disp="off")
        df_vol[col] = np.sqrt(res.conditional_volatility) / 100

    return df_vol