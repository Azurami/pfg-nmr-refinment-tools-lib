# Vladislav 29.12.20
# plots file, part of model, prepare data for visualisation
import itertools

import matplotlib.pyplot as plt
import os
import numpy as np
import matplotlib


# each spectrum has own dir
# def create_figures_dir(uuid, spectrum_number):
#     full_name_figures_dir = os.path.join('results/', uuid + str('/') + str(spectrum_number))
#     if not os.path.isdir(full_name_figures_dir):
#         os.mkdir(full_name_figures_dir)
#     return full_name_figures_dir

def create_figures_dir_not_ref(uuid, spectrum_number):
    full_name_figures_dir = os.path.join('results/', uuid + str('/') + 'not_ref')
    if not os.path.isdir(full_name_figures_dir):
        os.mkdir(full_name_figures_dir)
    return full_name_figures_dir

def create_figures_dir_ref(uuid, spectrum_number):
    full_name_figures_dir = os.path.join('results/', uuid + str('/') + 'ref')
    if not os.path.isdir(full_name_figures_dir):
        os.mkdir(full_name_figures_dir)
    return full_name_figures_dir

class Plotter:
    def __init__(self, uuid, left, right, converter, spectrum_number, peak_number):
        matplotlib.use('Agg')
        # matplotlib.use('TkAgg')
        self.spectrum_number = str(spectrum_number)
        # self.SAVE_DIR = create_figures_dir(uuid, spectrum_number)

        self.SAVE_DIR_NOT_REF = create_figures_dir_not_ref(uuid, spectrum_number)
        self.SAVE_DIR_REF = create_figures_dir_ref(uuid, spectrum_number)

        self.peak_number = peak_number
        self.converter = converter
        self.boundary_type = converter.boundary_type
        if self.boundary_type == "points":
            self.left = left
            self.right = right
        else:
            left, right = converter.convert_point_to_ppm(left, right)
            self.left = left
            self.right = right

    # def generate_png_file(self, postfix):
    #     # os.mkdir(self.SAVE_DIR)
    #     figure_file_name = os.path.join(self.SAVE_DIR, str(postfix) + '.png')
    #     return figure_file_name

    def generate_png_file_ref(self, postfix):
        # os.mkdir(self.SAVE_DIR)
        figure_file_name = os.path.join(self.SAVE_DIR_REF, str(postfix) +' (' +str(self.spectrum_number) + ').png')
        return figure_file_name

    def generate_png_file_not_ref(self, postfix):
        # os.mkdir(self.SAVE_DIR)
        figure_file_name = os.path.join(self.SAVE_DIR_NOT_REF, str(postfix) +' (' +str(self.spectrum_number) + ').png')
        return figure_file_name

    def plot_spectra(self, spectra):
        fig, ax = plt.subplots()
        spectra = np.array(spectra)
        spectrum_len = len(spectra[1, :])
        number_of_spectra = len(spectra[:, 1])
        # x = range(self.left, self.right)
        x = np.linspace(self.left, self.right, spectrum_len)
        if self.boundary_type == "ppm":
            ax.invert_xaxis()
            ax.set_xlabel("ppm")
        else:
            ax.set_xlabel("points")
        for i in range(0, number_of_spectra):
            ax.plot(x, spectra[i, :], linewidth=0.5)
        ax.set_title("Stack of spectra (integration region). Peak is " + self.peak_number+'. Spec No '+self.spectrum_number)
        spec_file_name = self.generate_png_file_not_ref('2. spectra_peak_'+self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name


    def plot_spectra_bl_corrected(self, spectra):
        fig, ax = plt.subplots()
        spectra = np.array(spectra)
        spectrum_len = len(spectra[1, :])
        number_of_spectra = len(spectra[:, 1])
        # x = range(self.left, self.right)
        x = np.linspace(self.left, self.right, spectrum_len)
        if self.boundary_type == "ppm":
            ax.invert_xaxis()
            ax.set_xlabel("ppm")
        else:
            ax.set_xlabel("points")
        for i in range(0, number_of_spectra):
            ax.plot(x, spectra[i, :], linewidth=0.5)
        ax.set_title("Stack of spectra (integration region) with bl correction. Peak is " + self.peak_number+'. Spec No '+self.spectrum_number)
        spec_file_name = self.generate_png_file_ref('5. spectra_peak_corrected_'+self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name

    def plot_full_spectra_and_region(self, spectra, left, right):
        fig, ax = plt.subplots()
        # spectra = np.array(spectra)
        full_spec_len = len(spectra[1, :])
        region_size = len(spectra[1, left:right])
        # x_full = range(0, spectrum_len)
        # x_to_integrate = range(left, right)
        if self.boundary_type == "points":
            full_x = np.linspace(0, full_spec_len, full_spec_len)
            x = np.linspace(left, right, region_size)
            ax.set_xlabel("points")
        else:
            full_x_left_ppm, full_x_right_ppm = self.converter.convert_point_to_ppm(0, full_spec_len)
            full_x = np.linspace(full_x_left_ppm, full_x_right_ppm, full_spec_len)
            left_point_in_points, right_point_in_points = self.converter.convert_point_to_ppm(left, right)
            x = np.linspace(left_point_in_points, right_point_in_points, region_size)
            ax.invert_xaxis()
            ax.set_xlabel("ppm")

        ax.plot(full_x, spectra[1, :], linewidth=0.5)
        ax.plot(x, spectra[1, left:right], linewidth=0.5, color='r')

        max_intensity_region = np.max(spectra[1, left:right])
        min_intensity_all = np.min(spectra[1, :])

        # ax.plot(x_full, spectra[1, :])
        # ax.plot(x_to_integrate, spectra[1, left:right], 'r')
        ax.set_ylim([1.05*min_intensity_all, 2.5*max_intensity_region])
        ax.set_title("Integration region is colored red. Peak is " + self.peak_number+'. Spec No '+self.spectrum_number)
        spec_file_name = self.generate_png_file_not_ref('1. full_spectra_peak_' + self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name

    def plot_integrals(self, grad, integrals):
        fig, ax = plt.subplots()
        ax.scatter(grad, integrals, marker='o')
        ax.set_title("Absolute integrals vs. gradients. Peak is " + self.peak_number+'. Spec No '+self.spectrum_number)
        ax.grid()
        ax.set_xlabel("Gradient, G/cm")
        ax.set_ylabel("Intensity")
        spec_file_name = self.generate_png_file_not_ref('3. integrals_peak_'+ self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name

    def plot_fitting_non_ref(self, grad, integrals, exp_func_value):
        fig, ax = plt.subplots()
        g = np.linspace(0, max(grad))
        ax.plot(grad, integrals, 'bo', label='Experimental data')
        ax.plot(g, exp_func_value, 'r-', label="fit")
        plt.title('Intensity decay. Data is not refiend. Peak is ' + self.peak_number+'. Spec No '+self.spectrum_number)
        ax.set_xlabel("Gradient, G/cm")
        ax.set_ylabel("Intensity")
        ax.grid()
        ax.legend()
        spec_file_name_not_ref_decay = self.generate_png_file_not_ref('4. not_ref_decay_peak_' + self.peak_number)
        fig.savefig(spec_file_name_not_ref_decay, dpi=600)
        plt.close()
        return spec_file_name_not_ref_decay

    def plot_ref_vs_not_ref_integrals(self, grad, integrals, integrals_refined):
        fig, ax = plt.subplots()
        ax.plot(grad, integrals, 'bo', label='Experimental data')
        ax.plot(grad, integrals_refined, 'r*', label="Refined Experimental data")
        plt.title('Refined values vs. not refined. Peak is ' + self.peak_number+'. Spec No '+self.spectrum_number)
        ax.set_xlabel("Gradient, G/cm")
        ax.set_ylabel("Intensity")
        ax.grid()
        ax.legend()
        spec_file_name_ref_vs_decay = self.generate_png_file_ref('6. Ref_vs_non-ref_peak' + self.peak_number)
        fig.savefig(spec_file_name_ref_vs_decay, dpi=600)
        plt.close()
        return spec_file_name_ref_vs_decay

    def plot_fitting_ref(self, grad, integrals, exp_func_value):
        fig, ax = plt.subplots()
        g = np.linspace(0, max(grad))
        ax.plot(grad, integrals, 'bo', label='Refined Experimental data')
        ax.plot(g, exp_func_value, 'r-', label="fit")
        plt.title('Data fit. Peak is ' + self.peak_number+'. Spec No '+self.spectrum_number)
        ax.set_xlabel("Gradient g, G/cm")
        ax.set_ylabel("Integrated signal")
        ax.grid()
        # ax.legend()
        spec_file_name_ref_decay = self.generate_png_file_ref('7. ref_decay_peak_'+ self.peak_number)
        fig.savefig(spec_file_name_ref_decay, dpi=600)
        plt.close()
        return spec_file_name_ref_decay

    def plot_fitting_ref_not_ref(self, grad, exp_func_value1,  exp_func_value2):
        fig, ax = plt.subplots()
        g = np.linspace(0, max(grad))
        ax.plot(g, exp_func_value1, 'r-', label="fit not ref")
        ax.plot(g, exp_func_value2, 'b-', label="fit ref")
        plt.title('Fittings. Peak is ' + self.peak_number+'. Spec No '+self.spectrum_number)
        ax.set_xlabel("Gradient g, G/cm")
        ax.set_ylabel("Integrated signal")
        ax.grid()
        ax.legend()
        spec_file_name_ref_decay = self.generate_png_file_ref('8. ref_and_not_ref_decay_peak_'+ self.peak_number)
        fig.savefig(spec_file_name_ref_decay, dpi=600)
        plt.close()
        return spec_file_name_ref_decay

    def plot_ideal_spectra(self, spectra):
        fig, ax = plt.subplots()
        spectra = np.array(spectra)
        spectrum_len = len(spectra[1, :])
        number_of_spectra = len(spectra[:, 1])
        # x = range(self.left, self.right)
        x = np.linspace(self.left, self.right, spectrum_len)
        if self.boundary_type == "ppm":
            ax.invert_xaxis()
            ax.set_xlabel("ppm")
        else:
            ax.set_xlabel("points")
        for i in range(0, number_of_spectra):
            ax.plot(x, spectra[i, :], linewidth=0.5)
        ax.set_title("Stack of IDEAL spectra (integration region). Peak is " + self.peak_number)
        spec_file_name = self.generate_png_file('9. spectra_peak_IDEAL_'+self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name

    def plot_residual_spectra(self, spectra):
        fig, ax = plt.subplots()
        spectra = np.array(spectra)
        spectrum_len = len(spectra[1, :])
        number_of_spectra = len(spectra[:, 1])
        # x = range(self.left, self.right)
        x = np.linspace(self.left, self.right, spectrum_len)
        if self.boundary_type == "ppm":
            ax.invert_xaxis()
            ax.set_xlabel("ppm")
        else:
            ax.set_xlabel("points")
        for i in range(0, number_of_spectra):
            ax.plot(x, spectra[i, :], linewidth=0.5)
        ax.set_title("Stack of residual spectra (integration region). Peak is " + self.peak_number)
        spec_file_name = self.generate_png_file('10. spectra_peak_residual_'+self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name

    def plot_mean_residual_spectra(self, spectra):
        fig, ax = plt.subplots()
        spectra = np.array(spectra)
        spectrum_len = len(spectra[1, :])
        number_of_spectra = len(spectra[:, 1])
        # x = range(self.left, self.right)
        x = np.linspace(self.left, self.right, spectrum_len)
        if self.boundary_type == "ppm":
            ax.invert_xaxis()
            ax.set_xlabel("ppm")
        else:
            ax.set_xlabel("points")
        for i in range(0, number_of_spectra):
            ax.plot(x, spectra[i, :], linewidth=0.5)
        ax.set_title("Stack of residual spectra (integration region). Peak is " + self.peak_number)
        spec_file_name = self.generate_png_file('11. spectra_peak_residual_'+self.peak_number)
        plt.savefig(spec_file_name, dpi=600)
        plt.close()
        return spec_file_name


