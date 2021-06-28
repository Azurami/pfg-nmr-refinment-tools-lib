# Vladislav 16.0.21
# Executor, performing all task to get refined diffusion coefficient
# INPUT: gamma, small_delta, big_delta, gradient_strength, spectra_full_file_name, difflist_full_file_name,
#        full_upload_dir_name, right_point, left_point
# OUTPUT: D_not_ref, A_not_ref, D_ref, A_ref, refined_integrals, difflist, plots_file_names
import os

from refinment.files_controller import make_uuid_dir
from refinment.plots import Plotter
from refinment.processing.data_reading import prepare_data_for_processing, get_data_for_processing, UnitConverter
from refinment.processing.processor import process_for_comparison
from tqdm import tqdm
import pandas as pd

from refinment.refinement import correct_baseline_full_spectra


def do_processing(right_point, left_point, acqu_dir_name, spc_dir_name, grad_shape_dir_name, prot_name, fit_type, converter, spectrum_number, peak_number):
    full_spectra, difflist, p1, p30, d16, d20, NS, RG = get_data_for_processing(acqu_dir_name, spc_dir_name, grad_shape_dir_name)
    gamma = 4258 # for 1H

    noise_left = [(4000, 6000)]
    noise_right = [(58000, 60000)]

    full_spectra = correct_baseline_full_spectra(full_spectra, noise_left, noise_right)

    sorted_sliced_spectra, sorted_difflist, sorted_full_spectra = prepare_data_for_processing(full_spectra, difflist, left_point, right_point)

    n_points = len(sorted_sliced_spectra[1,:])

    plotter = Plotter(prot_name, left_point, right_point, converter, spectrum_number, peak_number)
    plotter.plot_full_spectra_and_region(sorted_full_spectra, left_point, right_point)

    D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref = process_for_comparison(gamma, p30, d20, sorted_difflist, sorted_sliced_spectra, fit_type, p1, d16, plotter)

    return n_points, NS, RG, D_not_ref, SDE_not_ref, RMSD_not_ref, D_ref, SDE_ref, RMSD_ref




def run_processing(prot_name, path_to_datasets, spectra_id, peaks, fit_type):
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
                                    fit_type, converter, spectrum_number,peak_label)

            spectral_data_row = {'spectrum_id': spectrum_number,
                                 'area': peak_label,
                                 'n_points': n_points,
                                 'NS': NS,
                                 'RG': RG,
                                 'D_not_ref': D_not_ref,
                                 'SDE_not_ref': SDE_not_ref,
                                 'RMSD_not_ref': RMSD_not_ref,
                                 'D_ref': D_ref,
                                 'SDE_ref': SDE_ref,
                                 'RMSD_ref': RMSD_ref
                                 }
            df_new_row = pd.DataFrame(data=spectral_data_row, index=[spectrum_number])
            # df_spectral_data = df_spectral_data.append(df_new_row, ignore_index=True)
            df_new_row.to_csv(prot_name + '.csv', index=False, mode='a', header=not os.path.exists(prot_name + '.csv'))

    return 0
