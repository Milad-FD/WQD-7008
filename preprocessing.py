#!/usr/bin/ python3

import pandas as pd
import sys
from pathlib import Path
import numpy as np
import shutil

class Preprocess:
    def __init__(self,input_path, output_path) -> None:
      self.input_path =input_path
      self.output_path =output_path
      self.file_name = self.get_the_file_name(input_path)
      self.create_or_reset_path()

    def get_the_file_name(self,file_path=None):
        # Create a Path object from the file path
        path_obj = Path(file_path)
        # Get the name of the file
        return(path_obj.stem)
    
    def read_csv(self):
        self.df = pd.read_csv(self.input_path, sep=" ", header=None)

    def dropna(self):
        # Drop any extra columns created due to trailing spaces
        self.df.dropna(axis=1, how='all', inplace=True)

    def check_for_missing_value(self):
        # Checking for missing values
        missing_values = self.df.isnull()
        # Counting the number of missing values in each column
        return(missing_values.sum())
    
    def fill_in_missing_value_if_exist(self):
        # Check if there are any missing values
        if self.df.isnull().any().any():
            # Interpolate missing values in the DataFrame (inplace only if there are missing values)
            self.df.interpolate(inplace=True)
        
    def set_col_name(self,names=None):
        # ADD Column Name
        if names==None:
            self.df.columns = ['Engine', 'Cycle', 'OpSet1', 'OpSet2', 'OpSet3', 'SensorMeasure1', 'SensorMeasure2', 'SensorMeasure3', 'SensorMeasure4', 'SensorMeasure5', 'SensorMeasure6', 'SensorMeasure7', 'SensorMeasure8', 'SensorMeasure9', 'SensorMeasure10', 'SensorMeasure11', 'SensorMeasure12', 'SensorMeasure13', 'SensorMeasure14', 'SensorMeasure15', 'SensorMeasure16', 'SensorMeasure17', 'SensorMeasure18', 'SensorMeasure19', 'SensorMeasure20', 'SensorMeasure21']
        else:
            self.df.columns = names

    def get_maximum_cycle_per_engine(self):
        # Grouping by the 'ID' column and finding the max 'Cycle' value for each group
        result_max_cycle = self.df.groupby('Engine')['Cycle'].max()
        # Creating a new column 'EOL' and assigning the maximum 'Cycle' value for each 'ID' to it
        self.df['EOL'] = self.df['Engine'].map(result_max_cycle)

    def calculate_remaing_life_ratio_per_cycle(self):
        # Calculate "LR"
        self.df["LR"] = self.df["Cycle"].div(self.df["EOL"])

    def set_labels_base_on_ratio(self,good_condition_ratio = 0.6,moderate_condtion_ratio=0.8):
        # Good Condition - 0
        # Moderate Condition - 1
        # Warning Condition - 2
        labels=[]
        for i in range (0,len(self.df)):
            if np.array(self.df["LR"])[i] <= good_condition_ratio:
                labels.append(0)
            elif np.array(self.df["LR"])[i] <= moderate_condtion_ratio :
                labels.append(1)   
            else :
                labels.append(2)  
        self.df["labels"]=labels

    def drop_cols(self,cols=None):
        self.df  = self.df.drop(columns=cols)  

    def save(self,output_path = None):
        # Save the preprocessed data
        if output_path == None:
            self.df.to_csv(f"{self.output_path}/{self.file_name}_cleaned.csv", index=False)
        else:
            self.df.to_csv(f"{output_path}/{self.get_the_file_name(self.input_path)}_cleaned.csv", index=False)

    def create_or_reset_path(self):
        # Convert the input to a Path object
        path_obj = Path(self.output_path)
        # Check if the directory exists
        if path_obj.exists():
            # If it exists, delete the directory and its contents
            try:
                print(f"directory is not empty at {path_obj}")
                print("Deleting the files")
                shutil.rmtree(path_obj)
            except OSError as e:
                # Handle any errors that might occur during deletion
                print(f"Error: {e}")
                return
        # Create a new directory
        try:
            path_obj.mkdir(parents=True)
            print(f"Directory '{self.output_path}' created successfully.")
        except OSError as e:
            # Handle any errors that might occur during creation
            print(f"Error: {e}")

    def default_preprocess(self):
        self.read_csv()
        self.dropna()
        self.fill_in_missing_value_if_exist()
        self.set_col_name()
        self.get_maximum_cycle_per_engine()
        self.calculate_remaing_life_ratio_per_cycle()
        self.set_labels_base_on_ratio()
        self.drop_cols(['Engine','EOL','LR'])
        self.save()
       
if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise ValueError("Script requires two arguments: input and output file paths")
    # Command line arguments: input and output file paths
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    p = Preprocess(input_path, output_path)
    p.default_preprocess()