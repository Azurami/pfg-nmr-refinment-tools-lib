# Vladislav 15.02.21
# Compute integral from defined region

import numpy as np


def integrate(spectra):
    number_of_spectra = len(spectra[:, 1])
    integrals = []
    for i in range(0, number_of_spectra):
        integrals.append(sum(spectra[i, :]))
    return integrals


def normalize(integrals):
    integrals = np.array(integrals)
    normalized_integrals = integrals / max(integrals)
    return normalized_integrals

