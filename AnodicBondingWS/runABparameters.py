from matplotlib import axes
import loadCSVdata
import baselinefilter
import getparameters
import numpy as np

import matplotlib.pyplot as plt
from engineering_notation import EngNumber
from matplotlib.ticker import EngFormatter

if __name__ == "__main__":
    # Path with data obtained from Agilent DMM software
    csv_path = 'C:/Users/Hugo/PhD/TrabalhoPratico/AnodicBonding/GraficosCorrenteEletrica/Celulas/Si_1mm_Glass_500um_275C-1kV.csv'
    
    # Elapsed time and electric current values as numpy array
    time_data = loadCSVdata.LoadCSVData(path=csv_path).create_dataarray()[0]    #[0:29951]
    ec_raw_data = loadCSVdata.LoadCSVData(path=csv_path).create_dataarray()[1]  #[0:29951]

    # AsLS baseline filtering
    lambda_value = 0.6           # increase if data is too noisy
    p_value = 0.001
    n_iterations = 30
    ec_asls_filtered_data = baselinefilter.BaselineFiltering(ec_data=ec_raw_data).baseline_asls(
        lam=lambda_value, p=p_value, n_iter=n_iterations)
    ######np.savetxt("275-vacuo.csv", ec_asls_filtered_data, delimiter=";")

    # Parameter extraction from filtered data
    parameter_obj = getparameters.GetABParameters(time_values=time_data, ec_filtered_values=ec_asls_filtered_data)

    ## Peak electric current value, and corresponding elapsed time
    peak_ec_time_value, peak_ec_value, peak_ec_idx = parameter_obj.peak_value()
    print('Peak value: '+str(EngNumber(peak_ec_value))+'A'+" at "+str("%.2f" % peak_ec_time_value)+'s')

    ## Elapsed time at which half of the electric current was reached, corresponding electric current,
    ## and time difference between peak and half of electric current value
    fwhm_time_value, fwhm_ec_value, fwhm_time_diff, fwhm_idx = parameter_obj.fwhm_values()
    print("FWHM values: "+str(EngNumber(fwhm_ec_value))+'A'+" at "+str("%.2f" % fwhm_time_value)+'s')
    print("Peak and FWHM difference: "+str("%.2f" % fwhm_time_diff)+'s')

    ## Area under the signal from the peak to half of the electric current value
    area_signal = parameter_obj.area_under_signal()
    print("Area under signal peak-to-FWHM: "+str(EngNumber(area_signal))+'A.s'+" (electric current x time)")

    # Plotting all data
    fig, ax = plt.subplots()
    ax.plot(time_data, ec_raw_data, label='Raw data')
    ax.plot(time_data, ec_asls_filtered_data, label='AsLS filtered data')

    ax.plot(peak_ec_time_value, peak_ec_value, marker='o', color='tab:red')
    ax.plot(fwhm_time_value, fwhm_ec_value, marker='o', color='tab:red')
    ax.fill_between(time_data[peak_ec_idx:fwhm_idx], ec_asls_filtered_data[peak_ec_idx:fwhm_idx], alpha=0.5, color='lightgrey')
    
    
    ax.text(peak_ec_time_value, peak_ec_value, s=(str("%.2f" % peak_ec_time_value), str(EngNumber(peak_ec_value))), 
        weight='bold', fontsize='12')
    ax.text(fwhm_time_value, fwhm_ec_value, s=(str("%.2f" % fwhm_time_value), str(EngNumber(fwhm_ec_value))), 
        weight='bold', fontsize='12')
    ax.text((peak_ec_time_value+fwhm_time_value)/2, fwhm_ec_value, s="Area = "+str(EngNumber(area_signal))+'A.s',
        weight='bold', fontsize='12', ha='center', va='center')
    ax.legend(loc='best')
    ax.yaxis.set_major_formatter(EngFormatter(unit=''))
    ax.grid(alpha=0.5)

    plt.show()