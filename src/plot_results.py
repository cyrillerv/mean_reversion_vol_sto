import matplotlib.pyplot as plt

def plot_equity_curve(data, output_path="output/performance.png"):
    plt.figure(figsize=(10, 5))
    plt.plot(data.index, data["cumulative_returns"], label="Strategy")
    plt.title("Performance Cumulative")
    plt.legend()
    plt.grid()
    plt.savefig(output_path)
    plt.close()
