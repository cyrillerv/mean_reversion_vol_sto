import pandas as pd
from tqdm import tqdm
from backtesting.core import BacktestEngine # Librairy I created available on GitHub

from strats import *
from data_loader import *

df = load_data()

dic_fct_strats = {
    "first": first_strat, 
    "second": second_strat, 
    "third": third_strat,
    "SimpleVol": strat_vol,
    "GARCH": strat_vol
    }

# Arguments à passer à chaque stratégie
dic_args_fct = {
    "first": (df,), 
    "second": (df,), 
    "third": (df,), 
    "SimpleVol": (df, simple_vol),
    "GARCH": (df, calc_vol_garch)
}


dic_summary = {}
for name, strat in tqdm(dic_fct_strats.items()) :
    args = dic_args_fct[name]
    orders_df = strat(*args)
    engine = BacktestEngine(orders_df, df['close'], close_all=True)
    engine.run()
    dic_summary[name] = engine.summary()
df_res = pd.DataFrame(dic_summary)
df_res.to_excel(r"results\compTable.xlsx")