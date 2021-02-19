# Vladislav 29.12.20
# plots file, part of model, prepare data for visualisation

import matplotlib.pyplot as plt
import os, time
import numpy as np
import matplotlib
matplotlib.use('Agg')

plots_dir = 'figures'


def generate_png_file(postfix):
    if not os.path.isdir(plots_dir):
        os.mkdir(plots_dir)
        spec_file_name = os.path.join(plots_dir, str(time.time()) + str(postfix) + '.png')
    else:
        spec_file_name = os.path.join(plots_dir, str(time.time()) + str(postfix) + '.png')
    return spec_file_name


def plot_spectra(spectra):
    fig, ax = plt.subplots()
    spectra = np.array(spectra)
    spectrum_len = len(spectra[1, :])
    number_of_spectra = len(spectra[:, 1])
    x = range(0, spectrum_len)
    for i in range(0, number_of_spectra):
        ax.plot(x, spectra[i, :])
    ax.set_title("The region of the spectra to be integrated")
    spec_file_name = generate_png_file('spectra')
    plt.savefig(spec_file_name, dpi=600)
    plt.close()
    return spec_file_name


def plot_integrals(grad, integrals):
    fig, ax = plt.subplots()
    ax.scatter(grad, integrals, marker='o')
    ax.set_title("Absolute integrals vs. gradients")
    ax.grid()
    ax.set_xlabel("Gradient, G/cm")
    ax.set_ylabel("Intensity")
    spec_file_name = generate_png_file('integrals')
    plt.savefig(spec_file_name, dpi=600)
    plt.close()
    return spec_file_name


def plot_fitting_non_ref(grad, integrals, exp_func_value):
    fig, ax = plt.subplots()
    ax.plot(grad, integrals, 'bo', label='Experimental data')
    ax.plot(grad, exp_func_value, 'r-', label="fit")
    plt.title('Intensity decay. Data is not refiend')
    ax.set_xlabel("Gradient, G/cm")
    ax.set_ylabel("Intensity")
    ax.grid()
    ax.legend()
    spec_file_name_not_ref_decay = generate_png_file('not_ref_decay')
    fig.savefig(spec_file_name_not_ref_decay, dpi=600)
    plt.close()
    return spec_file_name_not_ref_decay


def plot_ref_vs_not_ref_integrals(grad, integrals, integrals_refined):
    fig, ax = plt.subplots()
    ax.plot(grad, integrals, 'bo', label='Experimental data')
    ax.plot(grad, integrals_refined, 'r*', label="Refined Experimental data")
    plt.title('Refined values vs. not refined')
    ax.set_xlabel("Gradient, G/cm")
    ax.set_ylabel("Intensity")
    ax.grid()
    ax.legend()
    spec_file_name_ref_vs_decay = generate_png_file('Ref_vs_non-ref')
    fig.savefig(spec_file_name_ref_vs_decay, dpi=600)
    plt.close()
    return spec_file_name_ref_vs_decay


def plot_fitting_ref(grad, integrals, exp_func_value):
    fig, ax = plt.subplots()
    ax.plot(grad, integrals, 'bo', label='Refined Experimental data')
    ax.plot(grad, exp_func_value, 'r-', label="fit")
    plt.title('Intensity decay. Data is refiend')
    ax.set_xlabel("Gradient, G/cm")
    ax.set_ylabel("Intensity")
    ax.grid()
    ax.legend()
    spec_file_name_ref_decay = generate_png_file('ref_decay')
    fig.savefig(spec_file_name_ref_decay, dpi=600)
    plt.close()
    return spec_file_name_ref_decay
