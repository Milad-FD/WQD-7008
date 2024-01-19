import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_and_save_sensors(input_dir, output_dir):
    # List of sensor names to plot
    sensor_names = [f'SensorMeasure{i}' for i in range(1, 22)]
    
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Plotting function
    def plot_sensor(sensor_name, data, base_filename):
        plt.figure(figsize=(13,5))
        for i in data['Engine'].unique():
            if i % 10 == 0:  # only plot every 10th unit_nr
                plt.plot('RUL', sensor_name, data=data[data['Engine']==i])
        plt.xlim(250, 0)  # reverse the x-axis so RUL counts down to zero
        plt.xticks(np.arange(0, 275, 25))
        plt.ylabel(sensor_name)
        plt.xlabel('Remaining Useful Life')
        # Save plot as PNG in the output directory
        plt.savefig(os.path.join(output_dir, f"{base_filename}_{sensor_name}.png"))
        plt.close()

    # Process each CSV file in the input directory
    for file_name in os.listdir(input_dir):
        if file_name.startswith('test') and file_name.endswith('.csv'):
            # Read the CSV file
            file_path = os.path.join(input_dir, file_name)
            test = pd.read_csv(file_path)
            # Calculate RUL
            test['max_cycle'] = test.groupby('Engine')['Cycle'].transform(max)
            test['RUL'] = test['max_cycle'] - test['Cycle']

            # Generate and save plots for each sensor
            base_filename = os.path.splitext(file_name)[0]  # Remove the .csv extension
            for sensor_name in sensor_names:
                plot_sensor(sensor_name, test, base_filename)

# Example usage
input_dir = '/home/ubuntu/Project7008/data/Processed'
output_dir = '/home/ubuntu/Project7008/data/Figures/Test'
plot_and_save_sensors(input_dir, output_dir)
