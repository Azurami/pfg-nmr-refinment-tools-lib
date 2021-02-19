# Vladislav 16.02.21
# main file

import sys
import argparse

from refinment.processing.data_reading import read_data_for_processing
from refinment.processing.data_writing import write_output_file, prepare_all_outputs
from refinment.processing.exectutor import do_processing
from refinment.processing.input_validation import validate

full_cmd_arguments = sys.argv
script_path = sys.path[0]

parser = argparse.ArgumentParser(description='Process pseudo 2d pfg nmr spectra and refine integrals to get refined D')
parser.add_argument('--gamma', type=float, dest='gamma', help='gamma (Hz/G)')
parser.add_argument('--small_delta', type=float, dest='small_delta', help='gradient pulse duration (s)')
parser.add_argument('--big_delta', type=float, dest='big_delta', help='diffusion time (s)')
parser.add_argument('--left_point', type=int, dest='left_point',
                    help='the right point of region for integration (in points)')
parser.add_argument('--right_point', type=int, dest='right_point',
                    help=' the left point of region for integration (in points)')
parser.add_argument('--specdir', type=str, dest='specdir', help='Input spectra dir')
parser.add_argument('--difflist', type=str, dest='difflist', help='Input difflist filename')
parser.add_argument('--resultsdir', type=str, dest='resultsdir', help='Output dir for results')
args = parser.parse_args()


def read_inputs(args):
    gamma = args.gamma
    small_delta = args.small_delta
    big_delta = args.big_delta
    right_point = args.right_point
    left_point = args.left_point
    spectra_full_file_name = script_path + args.specdir
    difflist_full_file_name = script_path + args.difflist
    results_output_dir = script_path + args.resultsdir
    return gamma, small_delta, big_delta, right_point, left_point, spectra_full_file_name, difflist_full_file_name, results_output_dir

#
gamma, small_delta, big_delta, right_point, left_point, spectra_full_file_name, difflist_full_file_name, output_dir_name = read_inputs(args)

full_spectra, gradients = read_data_for_processing(difflist_full_file_name, spectra_full_file_name)
pass_mark, msg = validate(gamma, small_delta, big_delta, full_spectra, gradients, left_point, right_point)

if pass_mark:
    outputs = do_processing(gamma, small_delta, big_delta, full_spectra,
                                gradients, left_point, right_point)
    CSV_results = write_output_file(outputs, output_dir_name)

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
else:
    print("Input error:"+msg)

