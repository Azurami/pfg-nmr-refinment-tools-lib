# Vladislav 16.02.21
# main file

import sys

from refinment.processing.data_writing import write_output_file, prepare_all_outputs
from refinment.processing.exectutor import do_processing

full_cmd_arguments = sys.argv
argument_list = full_cmd_arguments[1:]

script_path = sys.path[0]


def read_inputs(argument_list):
    gamma = float(argument_list[0])
    small_delta = float(argument_list[1])
    big_delta = float(argument_list[2])
    right_point = int(argument_list[4])
    left_point = int(argument_list[3])
    spectra_full_file_name = script_path+argument_list[5]
    difflist_full_file_name = script_path+argument_list[6]
    return gamma, small_delta, big_delta, right_point, left_point, spectra_full_file_name, difflist_full_file_name



gamma, small_delta, big_delta, right_point, left_point, spectra_full_file_name, difflist_full_file_name = read_inputs(argument_list)

outputs = do_processing(gamma, small_delta, big_delta, 0, difflist_full_file_name,
                        spectra_full_file_name, left_point, right_point)
A_not_ref, D_not_ref, A_ref, D_ref, refined_integrals, gradients, spectra_fig, integrals_fig, not_ref_decay_fig, ref_vs_not_ref_fig, \
ref_decay_fig = prepare_all_outputs(outputs)

print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~DONE!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(f"A not refine = {A_not_ref}")
print(f"D not refine = {D_not_ref} cm2/s")
print(f"A refined = {A_ref}")
print(f"D refined = {D_ref} cm2/s")
print("You can see the full results in 'Result' folder.")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~Warning! ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
print(" All files in 'Results' folder is removed after each script run.")
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~The END!~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")