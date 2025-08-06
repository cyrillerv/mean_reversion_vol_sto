import pandas as pd
from tqdm import tqdm
from backtesting.core import BacktestEngine # Librairy I created available on GitHub

from strats import *
from data_loader import *

list_fct_strats = {
    "first": first_strat, 
    "second": second_strat, 
    "third": third_strat,
    "GARCH": strat_garch_vol
    }

df = load_data()

dic_summary = {}
for name, strat in tqdm(list_fct_strats.items()) :
    orders_df = strat(df)
    engine = BacktestEngine(orders_df, df['close'], close_all=True)
    engine.run()
    dic_summary[name] = engine.summary()
df_res = pd.DataFrame(dic_summary)
df_res.to_excel(r"results\compTable.xlsx")