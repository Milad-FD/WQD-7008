import pandas as pd
import numpy as np
import sys
import socket
import time
from pathlib import Path
from sklearn.preprocessing import MinMaxScaler

class Postprocess:
    def __init__(self, input_dir, output_dir):
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.create_or_reset_path(output_dir)

    def get_files_by_prefix(self, prefix):
        path_obj = Path(self.input_dir)
        return list(path_obj.glob(f'{prefix}*.csv'))

    # def read_and_combine_csv(self, files):
    #     combined_df = pd.DataFrame()
    #     print("hello4")
    #     for file in files:
    #         print("hello5")
    #         df = pd.read_csv(file)
    #         print("hello6")
    #         combined_df = pd.concat([combined_df, df])
    #         print("hello7")
    #     return combined_df
    
    def read_and_combine_csv(self, files, prefix):
        combined_df = pd.DataFrame()
        files = self.get_files_by_prefix(prefix)  # Get files based on the given prefix
        for file in files:
            df = pd.read_csv(file)
            combined_df = pd.concat([combined_df, df])
        return combined_df 

    def normalize_columns(self, df, columns):
        scaler = MinMaxScaler()
        df[columns] = scaler.fit_transform(df[columns])
        return df

    def create_or_reset_path(self, path):
        path_obj = Path(path)
        if path_obj.exists():
            try:
                print(f"Directory exists at {path}")
            except OSError as e:
                print(f"Error: {e}")
                return
        else:
            try:
                path_obj.mkdir(parents=True)
                print(f"Directory '{path}' created successfully.")
            except OSError as e:
                print(f"Error: {e}")

    def save(self, df, filename):
        output_path = Path(self.output_dir) / filename
        if output_path.exists():
            try:
                print(f"File {filename} exists. Deleting the file.")
                output_path.unlink()
            except OSError as e:
                print(f"Error deleting file {filename}: {e}")
        
        df.to_csv(output_path, index=False)
        print(f"File {filename} saved successfully.")  # Added logging statement


    def process(self, prefix, columns_to_normalize):
        print(f"Processing prefix: {prefix}")  # Added logging statement
        files = self.get_files_by_prefix(prefix)
        combined_df = self.read_and_combine_csv(files,prefix)
        normalized_df = self.normalize_columns(combined_df, columns_to_normalize)
        self.save(normalized_df, f'{prefix}_combined.csv')

# def main():
#     input_dir = '/home/ubuntu/Project7008/data/Processed'  
#     output_dir = '/home/ubuntu/Project7008/data/Combined'  
#     columns_to_normalize = ['OpSet1','OpSet2','OpSet3'] 

#     postprocess = Postprocess(input_dir, output_dir)
#     postprocess.process('train', columns_to_normalize)
#     postprocess.process('test', columns_to_normalize)

# if __name__ == "__main__":
#     main()

# second try
# def main():
#     input_dir = '/home/ubuntu/Project7008/data/Processed'
#     output_dir = '/home/ubuntu/Project7008/data/Combined'
#     columns_to_normalize = ['OpSet1', 'OpSet2', 'OpSet3']
#     prefixes = ['train', 'test']
#     for prefix in prefixes:
#         postprocess = Postprocess(input_dir, output_dir)
#         postprocess.process(prefix, columns_to_normalize)

# if __name__ == "__main__":
#     main()

def main():
    hostname = socket.gethostname()
    if hostname == 'ip-172-31-57-29':
        prefix = 'train'
        time.sleep(5)
    elif hostname == 'ip-172-31-30-163':
        prefix = 'test'
        time.sleep(15)
    else:
        print(f"Unknown machine: {hostname}. Cannot determine prefix.")
        return    

    # prefix = sys.argv[1]
    input_dir = '/home/ubuntu/Project7008/data/Processed'
    output_dir = '/home/ubuntu/Project7008/data/Combined'
    columns_to_normalize = ['OpSet1', 'OpSet2', 'OpSet3']
    
    # if prefix not in ['train', 'test']:
    #     print(f"Invalid prefix: {prefix}. It should be 'train' or 'test'.")
    #     return
    
    postprocess = Postprocess(input_dir, output_dir)
    postprocess.process(prefix, columns_to_normalize)

if __name__ == "__main__":
    main()



