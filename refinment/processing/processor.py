# Vladislav 12.02.21
# Guide all actions in order to get refined diffusion coefficient from prepared data
# INPUT: gamma, small_delta, big_delta, gradients, spectra
# OUTPUT: D_not_ref, A_not_ref, D_ref, A_ref, refined_integrals, gradients, figure_full_names

from refinment.plots import plot_integrals, plot_fitting_non_ref, \
    plot_ref_vs_not_ref_integrals, plot_fitting_ref, plot_spectra
from refinment.fit import compute_beta, st_fit, fit_function
from refinment.integrate import normalize, integrate
from refinment.refinement import compute_mean_spectrum, refine


def process(gamma, small_delta, big_delta, gradients, spectra):
    fig_spectra = plot_spectra(spectra)
    integrals = integrate(spectra)
    fig_integrals = plot_integrals(gradients, integrals)

    normalized_integrals = normalize(integrals)
    beta = compute_beta(gamma, small_delta, big_delta)

    D_not_ref, A_not_ref = st_fit(gradients, normalized_integrals, beta)
    exp_function_not_ref = fit_function(gradients, A_not_ref, D_not_ref * beta)
    fig_not_ref_decay = plot_fitting_non_ref(gradients, normalized_integrals, exp_function_not_ref)

    mean_spectrum = compute_mean_spectrum(spectra, exp_function_not_ref)
    refined_integrals = refine(spectra, mean_spectrum)
    normalized_refined_integrals = normalize(refined_integrals)
    fig_ref_vs_decay = plot_ref_vs_not_ref_integrals(gradients, normalized_integrals, normalized_refined_integrals)

    D_ref, A_ref = st_fit(gradients, normalized_refined_integrals, beta)
    exp_function_ref = fit_function(gradients, A_ref, D_ref * beta)
    fig_ref_decay = plot_fitting_ref(gradients, normalized_refined_integrals, exp_function_ref)

    figure_full_names = [fig_spectra, fig_integrals, fig_not_ref_decay, fig_ref_vs_decay, fig_ref_decay]
    return A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients, figure_full_names
