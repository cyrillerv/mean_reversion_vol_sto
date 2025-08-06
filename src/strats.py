# source : https://www.youtube.com/watch?v=UkoTdKV65yk      
# problem: we open pos at the close while we need the close to calculate our signals => better to open position at the open the next day => could reduce performance

import pandas as pd

def first_strat(df_input) :
    df = df_input.copy()
    avg_HL_25 = (df['high'] - df['low']).rolling(25).mean()
    IBS = (df['close'] - df['low']) / (df['high'] - df['low'])
    Band = df['high'].rolling(25).max() - 2.5 * avg_HL_25
    entry_signals = (df['close'] < Band) & (IBS < 0.6)
    exit_signals = df['close'] > df['high'].shift(1)

    list_positions = []
    for ticker in entry_signals.columns:
        open_pos = False
        for enter, exit_, index in zip(entry_signals[ticker], exit_signals[ticker], entry_signals.index):
            if enter and exit_ :
                continue
            elif not open_pos and enter:
                open_pos = True
                list_positions.append({"Symbol": ticker, "Date": index, "Volume": 1, "Type": "Buy"})
            elif open_pos and exit_:
                open_pos = False
                list_positions.append({"Symbol": ticker, "Date": index, "Volume": 1, "Type": "Sell"})

    orders_df = pd.DataFrame(list_positions)
    return orders_df


def second_strat(df_input) :
    df = df_input.copy()
    IBS = (df['close'] - df['low']) / (df['high'] - df['low'])
    entry_signals = IBS > 0.9
    exit_signals = IBS <= 0.3

    list_positions = []
    for ticker in entry_signals.columns:
        open_pos = False
        for enter, exit_, index in zip(entry_signals[ticker], exit_signals[ticker], entry_signals.index):
            if enter and exit_ :
                continue
            elif not open_pos and enter:
                open_pos = True
                list_positions.append({"Symbol": ticker, "Date": index, "Volume": 1, "Type": "Sell"})
            elif open_pos and exit_:
                open_pos = False
                list_positions.append({"Symbol": ticker, "Date": index, "Volume": 1, "Type": "Buy"})

    orders_df = pd.DataFrame(list_positions)
    return orders_df

def third_strat(df_input) :
    df = df_input.copy()
    entry_signals = df['close'] < df['low'].rolling(window=5).min().shift(1)
    exit_signals = df['close'] > df['high'].shift(1)

    list_positions = []

    # Pour chaque ticker (chaque colonne dans entry_signals)
    for ticker in entry_signals.columns:
        open_pos = False
        holding_days = 0

        # Boucle sur les signaux pour ce ticker
        for date, (enter, exit_) in zip(entry_signals.index, zip(entry_signals[ticker], exit_signals[ticker])):

            # Si on a déjà une position ouverte
            if open_pos:
                holding_days += 1

                # Si condition de sortie remplie
                if exit_ or holding_days > 5:
                    list_positions.append({"Symbol": ticker, "Date": date, "Volume": 1, "Type": "Sell"})
                    open_pos = False
                    holding_days = 0

            # Si pas encore en position et condition d'entrée remplie
            elif enter:
                list_positions.append({"Symbol": ticker, "Date": date, "Volume": 1, "Type": "Buy"})
                open_pos = True
                holding_days = 1  # Commence à 1 car on vient d’ouvrir

    orders_df = pd.DataFrame(list_positions)
    return orders_df