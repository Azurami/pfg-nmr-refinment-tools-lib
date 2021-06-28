# Vladislav 15.02.21
# Performing refinement

import numpy as np


def compute_mean_spectrum(spectra, normalized_integrals):
    number_of_gradients = len(spectra[:, 1])
    spectra = np.transpose(spectra)
    w = []
    # Calculate the weights of the spectra for mean spectrum
    for i in range(0, number_of_gradients):
        w.append(normalized_integrals[i])
    w = w / sum(w)
    # Calculate the mean spectrum
    mean_spectrum = []
    for i in range(0, number_of_gradients):
        mean_spectrum.append(np.dot(w[i], spectra[:, i]))
    mean_spectrum = sum(mean_spectrum)
    return mean_spectrum

def correct_baseline(spectra):
    number_of_spectra = len(spectra[:, 1])
    corrected_spectra = []
    for i in range(0, number_of_spectra):
        spec_curr = spectra[i, :]
        spectrum_len = len(spec_curr)
        #baseline is a linear function y = a0+a1*x
        y_left = spec_curr[0]
        y_right = spec_curr[-1]

        a0 = y_left
        a1 = (y_right - y_left) / spectrum_len
        x = np.linspace(0, spectrum_len, spectrum_len)
        baseline = a0+a1*x;

        spec_curr = spec_curr - baseline;
        corrected_spectra.append(spec_curr)
    corrected_spectra = np.array(corrected_spectra)
    return corrected_spectra


def correct_baseline_full_spectra(spectra, left_noise, right_noise):
    number_of_spectra = len(spectra[:, 1])
    corrected_spectra = []
    for i in range(0, number_of_spectra):
        # spec_curr = spectra[i, left_noise[0][0]:right_noise[0][1]]
        spec_curr = spectra[i, :]
        spectrum_len = len(spec_curr[left_noise[0][0]:right_noise[0][1]])
        #baseline is a linear function y = a0+a1*x
        y_left_mean = np.mean(spec_curr[left_noise[0][0]:left_noise[0][1]])
        y_right_mean = np.mean(spec_curr[right_noise[0][0]:right_noise[0][1]])

        a0 = y_left_mean
        a1 = (y_right_mean - y_left_mean) / spectrum_len
        x = np.linspace(0, spectrum_len, spectrum_len)
        baseline = a0+a1*x;

        spec_curr[left_noise[0][0]:right_noise[0][1]] = spec_curr[left_noise[0][0]:right_noise[0][1]] - baseline;
        corrected_spectra.append(spec_curr)
    corrected_spectra = np.array(corrected_spectra)
    return corrected_spectra


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


def calculate_spectra(mean_spectrum, integrals):
    number_of_spectra = len(integrals)
    length_of_spectra = len(mean_spectrum)
    integrals = np.array(integrals)
    spectra = np.zeros((number_of_spectra,length_of_spectra))
    for i in range(0,number_of_spectra):
        spectra[i,:] = mean_spectrum*integrals[i]
    return spectra

def calculate_mean_spectra_of_noise(spectra):
    number_of_spectra = len(spectra[:,1])
    length_of_spectra = len(spectra[1,:])
    mean_spectral_noise = np.zeros((number_of_spectra,length_of_spectra))
    row_of_ones = np.ones((1,length_of_spectra))
    for i in range(0,number_of_spectra):
        mean_spectral_noise[i,:] = mean_spectral_noise[i,:] + row_of_ones*np.mean(spectra[i,:])
    return mean_spectral_noise