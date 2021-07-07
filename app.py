# Vladislav 16.06.21
# main file
import sys
from refinment.processing.exectutor import run_processing
import warnings
import time

if not sys.warnoptions:
    warnings.simplefilter("ignore")

prot_name = 'Lysozyme_peak1_apk2d_1st'
# prot_name = 'Lysozyme_residual_refinement_4'
# E.g. acqu_dir_name =  + str(spectrum_number) + '\\' after that spectrum_number is follow
path_to_datasets = 'C:\\NMR\\BioNMR\\IDPs_Refinement_series\\'
spectra_id = range(1,78)
# spectra_id = [32]

peaks = [(50100, 50900)] # peak 1 left-right points small-peak
# peaks = [(49100, 49790)] # peak 2 small-peak
# peaks = [(46030, 48900)] # peak 3 left-right points et-peak
# peaks = [(42900, 45900)] # peak 4 left-right points big-peak

# peaks = [(38490, 50900)] # large-peak peak 1-4 + sth else


fit_type = 'dstebp'

start_time = time.time()
run_processing(prot_name, path_to_datasets, spectra_id, peaks, fit_type)
print("--- Finished in %.2f seconds ---" % (time.time() - start_time))
