# Vladislav 29.12.20
# reading input files
# OUTPUT: sorted_sliced_spectra and stored_difflist

import numpy as np
import nmrglue as ng

def get_data_for_processing_CSV(acqu_dir_name, spc_dir_name, grad_shape_dir_name, spectrum_number, path_to_datasets):
    full_spectra, dic = read_data_for_processing_bruker(spc_dir_name)

    filename = path_to_datasets + 'C__NMR_BioNMR_IDPs_Refinement_series_'+str(spectrum_number)+'_ser'
    full_spectra = np.genfromtxt(filename + '.csv', delimiter='	', skip_header=1)
    spec_num = len(full_spectra[1, :])
    full_spectra = full_spectra[:, 1:spec_num - 1]
    full_spectra = np.transpose(full_spectra)
    full_spectra = np.flip(full_spectra, 1)

    p1, p30, d16, d20, NS, RG, GPNAM6 = read_params_for_processing(dic)
    difflist = read_difframp(GPNAM6, acqu_dir_name, grad_shape_dir_name)
    return full_spectra, difflist, p1, p30, d16, d20, NS, RG


def get_data_for_processing(acqu_dir_name, spc_dir_name, grad_shape_dir_name):
    full_spectra, dic = read_data_for_processing_bruker(spc_dir_name)
    p1, p30, d16, d20, NS, RG, GPNAM6 = read_params_for_processing(dic)
    difflist = read_difframp(GPNAM6, acqu_dir_name, grad_shape_dir_name)
    return full_spectra, difflist, p1, p30, d16, d20, NS, RG


def read_data_for_processing_bruker(data_directory):
    dic, data = ng.bruker.read_pdata(data_directory)
    full_spectra = data.real
    return full_spectra, dic

def read_params_for_processing(dic):
    p1 = dic['acqus']['P'][1] * 1e-6  # in seconds
    p30 = dic['acqus']['P'][30] * 1e-6  # in seconds
    d16 = dic['acqus']['D'][16]
    d20 = dic['acqus']['D'][20]
    GPNAM6 = dic['acqus']['GPNAM'][6]
    NS = dic['acqus']['NS']
    RG = dic['acqus']['RG']
    return p1, p30, d16, d20, NS, RG, GPNAM6



def read_difframp(GPNAM6, acqu_dir_name, grad_shape_dir_name):
    dic_shape = ng.fileio.jcampdx.read(grad_shape_dir_name+GPNAM6)
    shape_integfac = float(dic_shape[0]['_datatype_SHAPEDATA'][0]['$SHAPEINTEGFAC'][0])

    dic_difframp = ng.fileio.jcampdx.read(acqu_dir_name + 'Difframp')
    difframp_list = dic_difframp[0]['_datatype_SHAPEDATA'][0]['XYDATA'][0].split('\n')
    difframp_list.remove(difframp_list[0])
    difframp_list = [float(element) for element in difframp_list]
    difframp_list = np.array(difframp_list)

    CNST0 = 0.0189548 # for normal probe CNST0 = 0.0189548 cnst0 converts G/cm into numbers from 0 to 1

    relative_gradients = shape_integfac*difframp_list;
    difflist = relative_gradients/CNST0;
    return difflist

def prepare_data_for_processing(full_spectra, difflist, left_point, right_point):
    # sort
    difflist_index = np.argsort(difflist)
    sorted_difflist = np.sort(difflist)
    sorted_full_spectra = sort_list(full_spectra, difflist_index)
    # and slice
    sorted_sliced_spectra = slice_region_for_integration(sorted_full_spectra, left_point, right_point)
    return sorted_sliced_spectra, sorted_difflist, np.array(sorted_full_spectra)


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


class UnitConverter:
    def __init__(self, boundary_type):
        self.boundary_type = boundary_type

    def convert_ppm_to_points(self, data_directory, left_ppm, right_ppm):
            # Convert SW in Hz to SW in ppm, then add to left_boundary SW in ppm to get right boundary
            dic, data = ng.bruker.read_pdata(data_directory)
            number_of_points = data.shape[1]
            SW_in_HZ = dic["procs"]["SW_p"]
            Spectrometer_freq_in_MHz = dic["procs"]["SF"]
            SW_in_ppm = SW_in_HZ / Spectrometer_freq_in_MHz
            left_ppm_b = dic["procs"]["OFFSET"]
            right_ppm_b = dic["procs"]["OFFSET"] - SW_in_ppm
            # points(ppm) = -k * ppm + c, where k and c are the constant
            k = number_of_points / SW_in_ppm  # equal to number_of_points/(left_ppm_b - right_ppm_b) [points in ppm]
            c = number_of_points * 0.5 + number_of_points  * (right_ppm_b+left_ppm_b)/(2*(SW_in_ppm))

            left_point = -1*k * float(left_ppm) + c
            right_point = -1*k * float(right_ppm) + c

            self.k = k
            self.c = c

            return int(left_point), int(right_point)

    def convert_point_to_ppm(self, left, right):
        left_point = -1 * float(left) / self.k + self.c / self.k
        right_point = -1 * float(right) / self.k + self.c / self.k
        return float(left_point), float(right_point)


def form_peak_list(peak_borders):
    peak_number = len(peak_borders)

    First_point = []
    Last_point = []

    peaks = []

    area_number = 0;

    for i in range(0, peak_number):
        for j in range(i + 1, peak_number):
            if abs(i - j) == 1:
                area_number = area_number + 1
                peaks.append((peak_borders[i], peak_borders[j]))
                First_point.append(peak_borders[i])
                Last_point.append(peak_borders[j])

    for i in range(0, peak_number - 1):
        for j in range(i + 1, peak_number):
            if abs(i - j) != 1:
                area_number = area_number + 1
                peaks.append((peak_borders[i], peak_borders[j]))
                First_point.append(peak_borders[i])
                Last_point.append(peak_borders[j])
    return peaks
