# Vladislav 15.02.21
# Performing refinement

import numpy as np


def compute_mean_spectrum(spectra, exp_func_value):
    number_of_gradients = len(spectra[:, 1])
    spectra = np.transpose(spectra)
    w = []
    # Calculate the weights of the spectra for mean spectrum
    for i in range(0, number_of_gradients):
        w.append(exp_func_value[i])
    w = w / sum(w)
    # Calculate the mean spectrum
    mean_spectrum = []
    for i in range(0, number_of_gradients):
        mean_spectrum.append(np.dot(w[i], spectra[:, i]))
    mean_spectrum = sum(mean_spectrum)
    return mean_spectrum


def refine(spectra, mean_spectrum):
    number_of_gradients = len(spectra[:, 1])
    spectrum_len = len(spectra[1, :])
    x = np.linspace(0, 1, spectrum_len)
    corrected_spectrum = np.transpose(spectra)
    x = x / np.max(x)
    max_of_mean_spectrum = np.max(mean_spectrum)
    A = [np.ones(np.shape(x)), x, mean_spectrum / max_of_mean_spectrum]
    A = np.transpose(A)
    integrals_refined = []
    for i in range(0, number_of_gradients):
        B = corrected_spectrum[:, i] / max_of_mean_spectrum
        r = np.linalg.lstsq(A, B)
        integrals_refined.append(r[0][2])
    return integrals_refined
