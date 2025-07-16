import numpy as np
import pandas as pd
from scipy.optimize import minimize

def simulate_heston(S0, v0, mu, kappa, theta, sigma, rho, dt, N):
    """ Simule un prix et une variance selon Heston """
    S = np.zeros(N)
    v = np.zeros(N)
    S[0], v[0] = S0, v0

    for t in range(1, N):
        z1 = np.random.normal()
        z2 = rho * z1 + np.sqrt(1 - rho**2) * np.random.normal()

        v[t] = np.abs(v[t-1] + kappa * (theta - v[t-1]) * dt + sigma * np.sqrt(v[t-1] * dt) * z2)
        S[t] = S[t-1] * np.exp((mu - 0.5 * v[t-1]) * dt + np.sqrt(v[t-1] * dt) * z1)

    return S, v

def heston_loss(params, returns, dt):
    """ Fonction de perte entre returns simulés et réels """
    mu, kappa, theta, sigma, rho, v0 = params
    S0 = 100  # fictif
    N = len(returns)
    sim_prices, sim_vars = simulate_heston(S0, v0, mu, kappa, theta, sigma, rho, dt, N)
    sim_returns = np.diff(np.log(sim_prices))
    real_returns = returns[1:N]
    loss = np.mean((sim_returns - real_returns) ** 2)
    return loss

def calibrate_heston(returns, dt=1/252):
    """ Calibre le modèle de Heston sur des returns log """
    init_params = [
        0.0, # mu
        1.0, # kappa
        0.04, # theta
        0.2, # sigma
        -0.5, # rho
        0.04 # v0
        ] 
    bounds = [
    (-1, 1),     # mu    : drift raisonnable entre -100% et 100%
    (0.01, 5),   # kappa    : vitesse de reversion > 0
    (0.0001, 0.5), # theta  : variance long terme entre 1% et 70% annualisée
    (0.01, 1),   # sigma    : vol of vol entre 10% et 100%
    (-0.99, 0.99), # rho  : corrélation physique entre -1 et 1
    (0.0001, 0.5)  # v0 : variance initiale raisonnable
    ]


    result = minimize(heston_loss, init_params, args=(returns, dt), bounds=bounds, method='L-BFGS-B')
    return result.x  # return best params

def heston_vol(data):
    # We calculate the log returns.
    returns = np.log(data["price"]).diff().dropna().values
    params = calibrate_heston(returns)
    print("Paramètres Heston calibrés :", params)

    mu, kappa, theta, sigma, rho, v0 = params
    S0 = 100
    S_sim, v_sim = simulate_heston(S0, v0, mu, kappa, theta, sigma, rho, dt=1/252, N=len(data))

    data = data.copy()
    data["volatility"] = v_sim
    return data
