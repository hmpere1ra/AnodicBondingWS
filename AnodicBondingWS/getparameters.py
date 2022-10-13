import numpy as np
from scipy import integrate
import quadpy

class GetABParameters:
    def __init__(self, time_values, ec_filtered_values):
        self.time_data = time_values
        self.ec_filtered_data = ec_filtered_values          # Filtered electric current data to be processed

    def peak_value(self):       # Returns the maximum electric current value
        ec_max = np.max(self.ec_filtered_data)
        ec_max_idx = np.where(self.ec_filtered_data == ec_max)[0][0]
        ec_max_time = self.time_data[ec_max_idx]
        return ec_max_time, ec_max, ec_max_idx

    def fwhm_values(self):      # Returns the Full Width (time) at Half Maximum (of electric current) values
        half_peak = self.peak_value()[1]/2 
        fwhm_array_idx = np.abs(np.asarray(self.ec_filtered_data)-half_peak).argmin()
        fwhm_xvalue = self.time_data[fwhm_array_idx]    # Corresponding 'closest' time (FW)
        if self.peak_value()[0] < fwhm_xvalue:
            fwhm_yvalue = self.ec_filtered_data[fwhm_array_idx]
        else:
            fwhm_array_idx = np.where(self.ec_filtered_data == self.ec_filtered_data[-1])[0][0]
            fwhm_xvalue = self.time_data[fwhm_array_idx]
            fwhm_yvalue = self.ec_filtered_data[fwhm_array_idx]
        fwhm_time_diff = fwhm_xvalue-self.peak_value()[0]
        return fwhm_xvalue, fwhm_yvalue, fwhm_time_diff, fwhm_array_idx

    def area_under_signal(self):  # Integrating signal from Peak values to FWHM values
        integration_lower_lim_idx, integration_upper_lim_idx = [(np.where(self.time_data == self.peak_value()[0]))[0][0], 
            (np.where(self.time_data == self.fwhm_values()[0]))[0][0]]
        fwhm_time_array = self.time_data[integration_lower_lim_idx:integration_upper_lim_idx]          # FWHM time array for lower and upper integration boundaries
        fwhm_ec_array = self.ec_filtered_data[integration_lower_lim_idx:integration_upper_lim_idx]     # FWHM electric current array for integration
        return integrate.simps(fwhm_ec_array, x=fwhm_time_array, even='last')