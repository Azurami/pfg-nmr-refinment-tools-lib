# Vladislav 16.02.21
# write output files
# OUTPUT: A,D, refined A, refined D, refined integrals with gradients

import csv
import glob
import os
import time

# clear figures after n calculation
import numpy as np

n = 1;

dir_name = 'static'

def write_output_file(outputs):
    A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients = prepare_only_numerical_outputs(outputs)
    csv_file_name = generate_csv_file('results')
    with open(csv_file_name, mode='w') as results_file:
        # results_writer = csv.writer(results_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        results_writer = csv.writer(results_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        results_writer.writerow(['A not refine', A_not_ref])
        results_writer.writerow(['D not refine, cm2/s', D_not_ref])
        results_writer.writerow(['A refined', A_ref])
        results_writer.writerow(['D refined, cm2/s', D_ref])
        results_writer.writerow(['Integrals refined', form_array(refined_integrals)])
        results_writer.writerow(['Gradients', form_array(gradients)])
    remove_old_files()
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
    return A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients, spectra_fig, integrals_fig, \
           not_ref_decay_fig, ref_vs_not_ref_fig, ref_decay_fig


def prepare_only_numerical_outputs(outputs):
    A_not_ref = outputs[0]
    D_not_ref = outputs[1]
    A_ref = outputs[2]
    D_ref = outputs[3]
    refined_integrals = outputs[4]
    gradients = outputs[5]
    return A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients


def generate_csv_file(postfix):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
        scv_file_name = os.path.join(dir_name, str(time.time()) + str(postfix) + '.csv')
    else:
        scv_file_name = os.path.join(dir_name, str(time.time()) + str(postfix) + '.csv')
    return scv_file_name


def remove_old_files():
    path, dirs, files = next(os.walk(dir_name))
    file_count = len(files)
    if file_count > 6 * n:
        for filename in glob.glob(os.path.join(dir_name, '*.png')):
            os.remove(filename)
        for filename in glob.glob(os.path.join(dir_name, '*.csv')):
            os.remove(filename)
    return 0


def form_array(array):
    array_len = len(array)
    str_array = []
    for i in range(0, array_len):
        str_array.append(array[i])
    return str_array
