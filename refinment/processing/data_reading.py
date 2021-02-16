# Vladislav 29.12.20
# reading input files
# OUTPUT: sorted_sliced_spectra and stored_gradients

import numpy as np
import shutil
from zipfile import ZipFile


def read_data_for_processing(spec_file, grad_file, data_directory):
    gradients = np.genfromtxt(grad_file)
    spectra_number = len(gradients)

    # with ZipFile(spec_file, 'r') as zipObj:
    #     # Extract all the contents of zip file in current directory
    #     zipObj.extractall(data_directory)
    # zipObj.close()

    full_spectra = []
    for i in range(10001, 10001 + spectra_number):
        spectrum = np.genfromtxt((data_directory + '/' + str(i) + '/ascii-spec.txt'), delimiter=',')
        full_spectra.append(spectrum[:, 1])

    # try:
    #     shutil.rmtree(data_directory)
    # except OSError as e:
    #     print("Error:  %s" % e.strerror)

    return full_spectra, gradients


def prepare_data_for_processing(full_spectra, gradients, left_point, right_point):
    # sort
    grad_index = np.argsort(gradients)
    sorted_gradients = np.sort(gradients)
    sorted_full_spectra = sort_list(full_spectra, grad_index)
    # and slice
    sorted_sliced_spectra = slice_region_for_integration(sorted_full_spectra, left_point, right_point)
    return sorted_sliced_spectra, sorted_gradients


def sort_list(old_list, index):
    list_var = []
    len_array = len(index)
    for i in range(0, len_array):
        list_var.append(old_list[:][index[i]])
    return list_var


def slice_region_for_integration(spec, left, right):
    spec = np.array(spec)
    spec = spec[:, int(left):int(right)]
    return spec
