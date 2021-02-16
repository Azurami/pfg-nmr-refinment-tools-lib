# Vladislav 15.02.21
# Fitting procedure

import numpy as np
from scipy.optimize import curve_fit


def fit_function(x, a, d):
    return a * np.exp(-d * x * x)


def compute_beta(gamma, small_delta, big_delta):
    beta = np.power(2 * np.pi * gamma * small_delta, 2) * (big_delta - small_delta / 3);
    return beta


def st_fit(gradients, integrals, beta):
    popt, pcov = curve_fit(fit_function, gradients, integrals)
    params = popt
    params[1] = params[1] / beta
    A = params[0]
    D = params[1]
    return D, A
