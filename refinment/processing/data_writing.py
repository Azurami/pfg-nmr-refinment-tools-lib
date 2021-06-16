# Vladislav 16.02.21
# write output files
# OUTPUT: A,D, refined A, refined D, refined integrals with gradients

import csv
import os
import time

import numpy as np


def write_output_file(outputs, output_dir_name):
    A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients = prepare_only_numerical_outputs(outputs)
    refined_table = [gradients, refined_integrals]
    refined_table = np.transpose(refined_table)

    csv_file_name = generate_csv_file('refined_integrals', output_dir_name)

    np.savetxt(csv_file_name, refined_table, delimiter=",",  header="# Gradient [G/cm], Integrals [arbitrary units]")

    return csv_file_name


def write_output_file_only_integrals(outputs, output_dir_name):
    refined_integrals, gradients, fig_spectra, fig_integrals = prepare_integrals_only_outputs(outputs)
    refined_table = [gradients, refined_integrals]
    refined_table = np.transpose(refined_table)

    csv_file_name = generate_csv_file('refined_integrals', output_dir_name)

    np.savetxt(csv_file_name, refined_table, delimiter=",", header="# Gradient [G/cm], Integrals [arbitrary units]")

    return csv_file_name


def prepare_all_outputs(outputs):
    A_not_ref = outputs[0]
    D_not_ref = outputs[1]
    A_ref = outputs[2]
    D_ref = outputs[3]
    refined_integrals = outputs[4]
    gradients = outputs[5]
    spectra_fig = outputs[6][0]
    integrals_fig = outputs[6][1]
    not_ref_decay_fig = outputs[6][2]
    ref_vs_not_ref_fig = outputs[6][3]
    ref_decay_fig = outputs[6][4]
    STD_A_ref = outputs[7][0]
    STD_D_ref = outputs[7][1]
    return A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients, spectra_fig, integrals_fig, \
           not_ref_decay_fig, ref_vs_not_ref_fig, ref_decay_fig, STD_A_ref, STD_D_ref

def prepare_integrals_only_outputs(outputs):
    refined_integrals = outputs[0]
    gradients = outputs[1]
    fig_spectra = outputs[2]
    fig_integrals = outputs[3]
    return refined_integrals, gradients, fig_spectra, fig_integrals


def prepare_only_numerical_outputs(outputs):
    A_not_ref = outputs[0]
    D_not_ref = outputs[1]
    A_ref = outputs[2]
    D_ref = outputs[3]
    refined_integrals = outputs[4]
    gradients = outputs[5]
    return A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients


def generate_csv_file(postfix, output_dir_name):
    full_name_csv_dir = os.path.join(output_dir_name, str('csv'))
    os.mkdir(full_name_csv_dir)
    scv_file_name = os.path.join(full_name_csv_dir, str(postfix) + '.csv')
    return scv_file_name


def form_array(array):
    array_len = len(array)
    str_array = []
    for i in range(0, array_len):
        str_array.append(array[i])
    return str_array
