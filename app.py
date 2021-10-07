# Vladislav 16.06.21
# main file
import sys
from refinment.processing.exectutor import run_processing
import warnings
import time

if not sys.warnoptions:
    warnings.simplefilter("ignore")

# E.g. acqu_dir_name =  + str(spectrum_number) + '\\' after that spectrum_number is follow
path_to_datasets = 'C:\\NMR\\BioNMR\\IDPs_Refinement_series_zero_init_manual_phase_corr_spline_bpl_mestre\\'
spectra_id = range(1,78)
# spectra_id = [1000001]
fit_type = 'dstebp'

noise_wd = 40

peaks = [(50100, 50900),  (42900, 45900)] # peak 1 left-right points small-peak


# prot_name = 'Lys_TopSpin_ivan_manual_ph_by_mean_spline_blp_mestre'
# prot_name = 'Lys_TopSpin_ivan_manual_ph_by_mean_spline_blp_mestre_ideal'
label = 'TopSpin'


# prot_name = 'Lys_MestreNova_ivan_manual_ph_by_mean_blc_mpoints'
# # prot_name = 'Lys_MestreNova_ivan_manual_ph_by_mean_blc_mpoints_ideal'
# label = 'MestreNova'


start_time = time.time()
run_processing(prot_name, path_to_datasets, spectra_id, peaks, fit_type, noise_wd, label)
print("--- Finished in %.2f seconds ---" % (time.time() - start_time))
