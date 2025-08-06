import pandas as pd

def load_data() :
    df = pd.read_csv("SPY_NDX_FXI.csv", header=[0, 1])
    df.set_index(("Unnamed: 0_level_0", "Unnamed: 0_level_1"), inplace=True)
    df.index = pd.to_datetime(df.index)
    df.index.name = None
    return df