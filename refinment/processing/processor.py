# Vladislav 12.02.21
# Guide all actions in order to get refined diffusion coefficient from prepared data
# INPUT: gamma, small_delta, big_delta, gradient_strength, difflist, spectra, var_type, fit_type
# OUTPUT: D_not_ref, A_not_ref, D_ref, A_ref, refined_integrals, difflist, figure_full_names
import numpy as np

from refinment.fit import FitFunctionClassSTE, FitFunctionClassDSTEbp, FitFunctionClassDSTE, FitFunctionClassSTEbp, \
    FitFunctionClassSTEn, FitFunctionClassSTEbpn, FitFunctionClassDSTEn, FitFunctionClassDSTEbpn
from refinment.integrate import normalize, integrate
from refinment.refinement import compute_mean_spectrum, refine, correct_baseline


def process_for_comparison(gamma, p30, d20, gradients, spectra, fit_type, p1, d16, plotter):
    plotter.plot_spectra(spectra)
    integrals = integrate(spectra)
    plotter.plot_integrals(gradients, integrals)

    normalized_integrals = normalize(integrals)
    # standard
    if fit_type == 'ste':
        fitter = FitFunctionClassSTE(gamma, p30, d20)
    if fit_type == 'stebp':
        fitter = FitFunctionClassSTEbp(gamma, p30, d20, p1, d16)
    if fit_type == 'dste':
        fitter = FitFunctionClassDSTE(gamma, p30, d20, p1, d16)
    if fit_type == 'dstebp':
        fitter = FitFunctionClassDSTEbp(gamma, p30, d20, p1, d16)
    # non-standard
    if fit_type == 'nste':
        fitter = FitFunctionClassSTEn(gamma, p30, d20)
    if fit_type == 'nstebp':
        fitter = FitFunctionClassSTEbpn(gamma, p30, d20, d16)
    if fit_type == 'ndste':
        fitter = FitFunctionClassDSTEn(gamma, p30, d20, d16)
    if fit_type == 'ndstebp':
        fitter = FitFunctionClassDSTEbpn(gamma, p30, d20, p1, d16)

    A_not_ref, D_not_ref, exp_function_not_ref, pcov_not_ref, RMSD_not_ref = fitter.fit(gradients, normalized_integrals)
    plotter.plot_fitting_non_ref(gradients, normalized_integrals, exp_function_not_ref)

    spectra = correct_baseline(spectra)
    integrals = integrate(spectra)
    normalized_integrals = normalize(integrals)

    mean_spectrum = compute_mean_spectrum(spectra, normalized_integrals)
    refined_integrals = refine(spectra, mean_spectrum)
    normalized_refined_integrals = normalize(refined_integrals)
    plotter.plot_ref_vs_not_ref_integrals(gradients, normalized_integrals, normalized_refined_integrals)

    A_ref, D_ref, exp_function_ref, pcov_ref, RMSD_ref = fitter.fit(gradients, normalized_refined_integrals)
    plotter.plot_fitting_ref(gradients, normalized_refined_integrals, exp_function_ref)

    SDE_not_ref = np.sqrt(np.diag(pcov_not_ref))[1]
    SDE_ref = np.sqrt(np.diag(pcov_ref))[1]

    return D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref

