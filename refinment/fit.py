# Vladislav 25.02.21
# Fitting procedure

import numpy as np
from scipy.optimize import curve_fit


class FitFunctionClassAbstract:
    def __init__(self, gamma, small_delta, big_delta):
        self.fit_function = None
        self.gamma = gamma
        self.small_delta = small_delta
        self.big_delta = big_delta

    def fit(self, difflist, integrals):
        initial_parameters = np.array([1.0, 1e-6])
        popt, pcov = curve_fit(self.fit_function, difflist, integrals, initial_parameters)
        params = popt
        A = params[0]
        D = params[1]
        g = np.linspace(0, max(difflist))
        y = self.fit_function(g, A, D)
        y_for_rmsd = self.fit_function(difflist, A, D)
        RMSD = self.rmsd_calculation(integrals, y_for_rmsd)
        y = y / A
        return A, D, y, pcov, RMSD

    def rmsd_calculation(self, integrals, function):
        # stats (from other answer)
        absError = integrals - function
        SE = np.square(absError)  # squared errors
        MSE = np.mean(SE)  # mean squared errors
        RMSD = np.sqrt(MSE)  # Root Mean Squared Deviation, RMSD
        return RMSD


# standard
class FitFunctionClassSTE(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta):
        super().__init__(gamma, small_delta, big_delta)
        self.fit_function = self.fit_function_ste_gradients

    def function_ste(self, gamma, small_delta, big_delta, gradients, A, D):
        return A * np.exp(-1 * (2*np.pi*gamma * small_delta * gradients) ** 2 * (big_delta - small_delta / 3) * D)

    def fit_function_ste_gradients(self, gradients, A, D):
        return self.function_ste(self.gamma, self.small_delta, self.big_delta, gradients, A, D)


class FitFunctionClassSTEbp(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, p1, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.fit_function = self.fit_function_ste_gradients
        self.d16 = d16
        self.p1 = p1

    def function_stebp(self, gamma, small_delta, big_delta, gradients, A, D, d16, p1):
        d20 = big_delta
        p30 = small_delta
        return A * np.exp(-1 * (2*np.pi*gamma * 2 * p30 * gradients) ** 2 * (d20 - 2 * p30 / 3 - d16 / 2 - 4 * p1) * D)

    def fit_function_ste_gradients(self, gradients, A, D):
        return self.function_stebp(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.d16, self.p1)


class FitFunctionClassDSTE(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, p1, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.p1 = p1
        self.d16 = d16
        self.fit_function = self.fit_function_dste_gradients

    def function_dste(self, gamma, small_delta, big_delta, gradients, A, D, p1, d16):
        DELAY20 = big_delta
        PULSE30 = small_delta
        DELAY16 = d16  # delay for gradient recovery
        PULSE1 = p1  # duration of 90 degree pulse
        alpha = 2 * np.pi*gamma * PULSE30 * gradients
        beta = DELAY20 - 5 / 3 * PULSE30 - DELAY16 - 4 * PULSE1
        return A * np.exp(-alpha ** 2 * beta * D)

    def fit_function_dste_gradients(self, gradients, A, D):
        return self.function_dste(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.p1, self.d16)

class FitFunctionClassDSTEbp(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, p1, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.p1 = p1
        self.d16 = d16
        self.fit_function = self.fit_function_dste_gradients

    def function_dste_bp(self, gamma, small_delta, big_delta, gradients, A, D, p1, d16):
        DELAY20 = big_delta
        PULSE30 = small_delta
        DELAY16 = d16  # delay for gradient recovery
        PULSE1 = p1  # duration of 90 degree pulse
        alpha = 2 * np.pi * gamma * (2 * PULSE30) * gradients
        beta = DELAY20 - 10/3 * PULSE30 - 3 * DELAY16 - 8 * PULSE1
        return A * np.exp(-alpha ** 2 * beta * D)

    def fit_function_dste_gradients(self, gradients, A, D):
        return self.function_dste_bp(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.p1, self.d16)

# non-standard
# small_delta = small_delta, big_delta = big_T, d16 = tau1, p1 = tau2
class FitFunctionClassSTEn(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta):
        super().__init__(gamma, small_delta, big_delta)
        self.fit_function = self.fit_function_ste_gradients

    def function_ste_n(self, gamma, small_delta, big_delta, gradients, A, D):
        return A * np.exp(-1 * (2*np.pi*gamma * small_delta * gradients) ** 2 * (big_delta - small_delta / 3) * D)

    def fit_function_ste_gradients(self, gradients, A, D):
        return self.function_ste_n(self.gamma, self.small_delta, self.big_delta, gradients, A, D)


class FitFunctionClassSTEbpn(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.fit_function = self.fit_function_ste_gradients
        self.d16 = d16


    def function_stebp_n(self, gamma, small_delta, big_delta, gradients, A, D, d16):
        T = big_delta
        tau = d16
        return A * np.exp(-1 * (2*np.pi*gamma * small_delta * gradients) ** 2 * (T + 2 * small_delta / 3 + 3 * tau / 4 ) * D)

    def fit_function_ste_gradients(self, gradients, A, D):
        return self.function_stebp_n(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.d16)


class FitFunctionClassDSTEn(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.d16 = d16
        self.fit_function = self.fit_function_dste_gradients

    def function_dste_n(self, gamma, small_delta, big_delta, gradients, A, D, d16):
        T = big_delta
        tau = d16
        alpha = 2 * np.pi*gamma * small_delta * gradients
        beta = T + 4 / 3 * small_delta + 2 * tau
        return A * np.exp(-alpha ** 2 * beta * D)

    def fit_function_dste_gradients(self, gradients, A, D):
        return self.function_dste_n(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.d16)

class FitFunctionClassDSTEbpn(FitFunctionClassAbstract):
    def __init__(self, gamma, small_delta, big_delta, p1, d16):
        super().__init__(gamma, small_delta, big_delta)
        self.p1 = p1
        self.d16 = d16
        self.fit_function = self.fit_function_dste_gradients

    def function_dste_bp_n(self, gamma, small_delta, big_delta, gradients, A, D, p1, d16):
        T = big_delta
        tau1 = d16
        tau2 = p1
        alpha = 2 * np.pi*gamma * small_delta * gradients
        beta = T + 4/3 * small_delta + 5/4 * tau1 + tau2 / 4
        return A * np.exp(-alpha ** 2 * beta * D)

    def fit_function_dste_gradients(self, gradients, A, D):
        return self.function_dste_bp_n(self.gamma, self.small_delta, self.big_delta, gradients, A, D, self.p1, self.d16)