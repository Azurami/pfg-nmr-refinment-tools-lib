# Vladislav 16.02.21
# Executor, performing all task to get refined diffusion coefficient
# INPUT: gamma, small_delta, big_delta, spectra_full_file_name, difflist_full_file_name,
#        full_upload_dir_name, right_point, left_point
# OUTPUT: D_not_ref, A_not_ref, D_ref, A_ref, refined_integrals, gradients, plots_file_names

from refinment.processing.data_reading import read_data_for_processing, prepare_data_for_processing
from refinment.processing.data_writing import write_output_file
from refinment.processing.processor import process


def do_processing(gamma, small_delta, big_delta, spectra_full_file_name, difflist_full_file_name, full_upload_dir_name, right_point, left_point):
    full_spectra, gradients = read_data_for_processing(spectra_full_file_name, difflist_full_file_name, full_upload_dir_name)
    sorted_sliced_spectra, sorted_gradients = prepare_data_for_processing(full_spectra, gradients, right_point, left_point)
    outputs = process(gamma, small_delta, big_delta, sorted_gradients, sorted_sliced_spectra)
    # write_output_file(outputs)
    # outputs = [ A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, figure_full_names ]
    return outputs
