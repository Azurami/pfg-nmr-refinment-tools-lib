# Vladislav 16.0.21
# Executor, performing all task to get refined diffusion coefficient
# INPUT: gamma, small_delta, big_delta, gradient_strength, spectra_full_file_name, difflist_full_file_name,
#        full_upload_dir_name, right_point, left_point
# OUTPUT: D_not_ref, A_not_ref, D_ref, A_ref, refined_integrals, difflist, plots_file_names
import os

import numpy as np

from refinment.files_controller import make_uuid_dir
from refinment.plots import Plotter
from refinment.processing.data_reading import prepare_data_for_processing, get_data_for_processing, UnitConverter, \
    get_data_for_processing_CSV, get_data_for_processing_from_1rr
from refinment.processing.processor import process_for_comparison
from tqdm import tqdm
import pandas as pd

from refinment.refinement import get_mean_y, global_baseline_correction, global_baseline_correction_as_in_Matlab


def do_processing(right_point, left_point, acqu_dir_name, spc_dir_name, grad_shape_dir_name, prot_name, fit_type, converter, spectrum_number, peak_number, noise_wd, path_to_datasets):
    spc_no_start= 10001
    spc_number = 20
    spc_1D_dir_name = path_to_datasets + str(spectrum_number) + '\\pdata\\'

    # TopSpin
    # full_spectra, difflist, p1, p30, d16, d20, NS, RG = get_data_for_processing(acqu_dir_name, spc_dir_name, grad_shape_dir_name)

    # TopSpin from 1rr stack
    full_spectra, difflist, p1, p30, d16, d20, NS, RG = get_data_for_processing_from_1rr(acqu_dir_name, spc_dir_name,
                                                                                grad_shape_dir_name, spc_no_start,
                                                                                         spc_number, spc_1D_dir_name)


    # MestreNova
    # full_spectra, difflist, p1, p30, d16, d20, NS, RG = get_data_for_processing_CSV(acqu_dir_name, spc_dir_name, grad_shape_dir_name, spectrum_number, path_to_datasets)


    # full_spectra = global_baseline_correction_as_in_Matlab(full_spectra, noise_wd, right_point, left_point)
    # right_point_noise = 10000
    # left_point_noise = 60000
    # noise_wd_global = 2000
    # full_spectra = global_baseline_correction(full_spectra, noise_wd_global, right_point_noise, left_point_noise)

    gamma = 4258  # for 1H

    y_left_mean, y_right_mean = get_mean_y(full_spectra, noise_wd, right_point, left_point)

    sorted_sliced_spectra, sorted_difflist, sorted_full_spectra = prepare_data_for_processing(full_spectra, difflist, left_point, right_point)

    # n = 4
    #
    # sorted_sliced_spectra, sorted_difflist, sorted_full_spectra = exclude_first_n(sorted_sliced_spectra, sorted_difflist, sorted_full_spectra, n)

    # n = 3
    # sorted_sliced_spectra, sorted_difflist, sorted_full_spectra =  exclude_first_n_with_first(sorted_sliced_spectra, sorted_difflist, sorted_full_spectra, n)
    n_points = len(sorted_sliced_spectra[1,:])

    plotter = Plotter(prot_name, left_point, right_point, converter, spectrum_number, peak_number)
    plotter.plot_full_spectra_and_region(sorted_full_spectra, left_point, right_point)

    D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref = process_for_comparison(gamma, p30, d20,
        sorted_difflist, sorted_sliced_spectra, fit_type, p1, d16, plotter, y_left_mean, y_right_mean)
    # D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref = 0,0,0,0,0,0
    return n_points, NS, RG, D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref


def exclude_first_n_with_first(sorted_sliced_spectra, sorted_difflist, sorted_full_spectra, n):
    n_spectra = len(sorted_difflist)

    sorted_sliced_spectra = np.delete(sorted_sliced_spectra, (1, n), 0)
    sorted_difflist = np.delete(sorted_difflist, (1, n), 0)
    sorted_full_spectra = np.delete(sorted_full_spectra, (1, n), 0)


    return sorted_sliced_spectra, sorted_difflist, sorted_full_spectra


def exclude_first_n(sorted_sliced_spectra, sorted_difflist, sorted_full_spectra, n):
    n_spectra = len(sorted_difflist)
    sorted_sliced_spectra = sorted_sliced_spectra[n:n_spectra,:]
    sorted_difflist = sorted_difflist[n:n_spectra]
    sorted_full_spectra = sorted_full_spectra[n:n_spectra,:]
    return sorted_sliced_spectra, sorted_difflist, sorted_full_spectra

def run_processing(prot_name, path_to_datasets, spectra_id, peaks, fit_type, noise_wd, label):
    make_uuid_dir(prot_name)
    number_of_spectra = len(spectra_id)
    df_spectral_data = pd.DataFrame()
    for spectrum_number in tqdm(spectra_id):
        acqu_dir_name = path_to_datasets + str(spectrum_number) + '\\'
        spc_dir_name = path_to_datasets + str(spectrum_number) + '\\pdata\\1'
        grad_shape_dir_name = "C:\\NMR\\exp\\stan\\nmr\\lists\\gp\\"
        number_of_peaks = len(peaks)
        print(f'\nSpectrum {spectrum_number} of {number_of_spectra}')
        for index, peak in enumerate(peaks):
            left_point = peak[0]
            right_point = peak[1]
            boundary_type ='points'
            converter = UnitConverter(boundary_type)
            peak_label = str(left_point) + '-' + str(right_point)
            print(f'\nPeak {index+1} of {number_of_peaks}')
            n_points, NS, RG, D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref = \
                do_processing(right_point, left_point, acqu_dir_name,
                                    spc_dir_name, grad_shape_dir_name, prot_name,
                                    fit_type, converter, spectrum_number, peak_label, noise_wd, path_to_datasets)

            spectral_data_row = {'spectrum_id': spectrum_number,
                                 'area': peak_label,
                                 'n_points': n_points,
                                 'NS': NS,
                                 'RG': RG,
                                 'D_not_ref': D_not_ref,
                                 'SDE_not_ref': SDE_not_ref,
                                 'RMSD_not_ref': RMSD_not_ref,
                                 'BLC points': noise_wd,
                                 'D_ref': D_ref,
                                 'SDE_ref': SDE_ref,
                                 'RMSD_ref': RMSD_ref,
                                 'Spftware':label
                                 }
            df_new_row = pd.DataFrame(data=spectral_data_row, index=[spectrum_number])
            # df_spectral_data = df_spectral_data.append(df_new_row, ignore_index=True)
            df_new_row.to_csv(prot_name + '.csv', index=False, mode='a', header=not os.path.exists(prot_name + '.csv'))

    return 0
