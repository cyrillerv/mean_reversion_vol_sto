import matplotlib.pyplot as plt

def plot_equity_curve(data, output_path="output/performance.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["cumulative_returns"], label="Strategy")
    plt.title("Performance Cumulative")
    plt.legend()
    plt.grid()
    plt.savefig(output_path)
    plt.close()

def plot_volatility(data, output_path="output/volatility_estimate.png"):
    plt.figure(figsize=(10, 4))
    plt.plot(data.index, data["volatility"], label="Volatility")
    plt.title("Volatilité estimée (Heston)")
    plt.grid()
    plt.legend()
    plt.savefig(output_path)
    plt.close()

def plot_signals(data, output_path="output/trading_signals.png"):
    """
    Trace les signaux de trading sur le prix de l'actif.

    Affiche :
    - Le prix de l’actif.
    - La moyenne mobile utilisée dans la stratégie de mean reversion.
    - Les bandes de ±1×volatilité autour de la moyenne mobile.
    - Les points d’entrée (achat) et de sortie (vente) identifiés par la stratégie.

    Args:
        data (pd.DataFrame): Données avec colonnes 'price', 'ma', 'volatility', 'signal'.
        output_path (str): Chemin de sauvegarde du graphique généré.
    """
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["price"], label="Prix", color="black", linewidth=1)
    plt.plot(data.index, data["ma"], label="Moyenne mobile", color="blue", linestyle="--")
    
    # Bandes de volatilité
    upper_band = data["ma"] + data["volatility"]
    lower_band = data["ma"] - data["volatility"]
    plt.fill_between(data.index, lower_band, upper_band, color="lightblue", alpha=0.3, label="±1×Volatilité")

    # Signaux
    buy_signals = data[data["signal"] == 1]
    sell_signals = data[data["signal"] == -1]
    plt.scatter(buy_signals.index, buy_signals["price"], marker="^", color="green", label="Signal Achat", zorder=5)
    plt.scatter(sell_signals.index, sell_signals["price"], marker="v", color="red", label="Signal Vente", zorder=5)

    plt.title("Signaux de Trading – Mean Reversion")
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()


def plot_results(data) :
    plot_equity_curve(data)
    plot_volatility(data)
    plot_signals(data)