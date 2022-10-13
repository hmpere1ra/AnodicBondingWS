import pandas as pd

class LoadCSVData:
    def __init__(self, path):
        self.data_path = path                                           # CSV file path

    def create_dataframe(self):
        data_frame = pd.read_csv(self.data_path, sep=';', decimal=",")  # CSV comes with semicolumn separation and column decimal separation
        #data_frame = data_frame.drop(labels='Unnamed: 2', axis=1)       # function returned 3rd unwanted 'Unnamed: 2' column
        data_array = data_frame.to_numpy()                              # converting df to array for easier data handling
        return data_array

    def create_dataarray(self):
        time_values = self.create_dataframe()[:,0]                      # first to_numpy() array corresponds to elapsed time of measure
        current_values = self.create_dataframe()[:,1]                   # second to_numpy() array corresponds to measured current values
        return time_values, current_values
