# Vladislav 16.06.21
# main file
import sys
from refinment.processing.exectutor import run_processing
import warnings
import time

if not sys.warnoptions:
    warnings.simplefilter("ignore")

prot_name = 'Lysozyme_small_peak_49100_49790_3rd'
# prot_name = 'Lysozyme_residual_refinement_4'
# E.g. acqu_dir_name =  + str(spectrum_number) + '\\' after that spectrum_number is follow
path_to_datasets = 'C:\\NMR\\BioNMR\\IDPs_Refinement_series\\'
spectra_id = range(1,78)
# spectra_id = [1]

# peaks = [(50200, 50850)] # left-right points small-peak
# peaks = [(42900, 45900)] # left-right points big-peak
# peaks = [(46030, 48900)] # left-right points et-peak
# peaks = [(42900, 48900)] # left-right points large-peak
# peaks = [(42900, 45280)]
peaks = [(49100, 49790)]

fit_type = 'dstebp'

start_time = time.time()
run_processing(prot_name, path_to_datasets, spectra_id, peaks, fit_type)
print("--- Finished in %.2f seconds ---" % (time.time() - start_time))
