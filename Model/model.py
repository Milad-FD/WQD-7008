import pandas as pd
import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score

class DataProcessor:
    def __init__(self, input_dir, file_name):
        self.input_dir = input_dir
        self.file_name = file_name
        self.df = self.read_CSV_()

    def read_CSV_(self):
        # Read the CSV file
        file_path = os.path.join(self.input_dir, self.file_name)
        return pd.read_csv(file_path)

    def drop_cols(self, cols=None):
        self.df = self.df.drop(columns=cols)

    def default_preprocess(self):
        self.drop_cols(['Engine'])

def create_output_directory(output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

def train_models(X_train, y_train):
    RF = RandomForestClassifier()
    DT = DecisionTreeClassifier()
    LR = LogisticRegression()
    RF.fit(X_train, y_train)
    DT.fit(X_train, y_train)
    LR.fit(X_train, y_train)
    return RF, DT, LR

# def evaluate_model(model, X_test, y_test, colormap, output_dir, model_name):
#     y_pred = model.predict(X_test)
#     cm = pd.DataFrame(confusion_matrix(y_test, y_pred, normalize='true')*100)
#     sns.heatmap(cm, annot=True, cmap=colormap)
#     # Adding titles and labels
#     plt.title(f'Confusion Matrix for {model_name}')
#     plt.xlabel('Predicted Label')
#     plt.ylabel('True Label')
#     plt.savefig(os.path.join(output_dir, f'confusion_matrix_{model_name}.png'))
#     plt.clf()  # Clear the current figure
#     accuracy = accuracy_score(y_test, y_pred)
#     return accuracy

# def test_on_new_dataset(test_data_dir, test_file_name, models, output_dir):
#     # Load and preprocess test dataset
#     test_processor = DataProcessor(test_data_dir, test_file_name)
#     test_processor.default_preprocess()
#     X_test_new = test_processor.df.iloc[:, 0:-1]
#     y_test_new = test_processor.df.iloc[:, -1]

#     # Evaluate each model on the new dataset
#     for model_name, model in models.items():
#         accuracy = evaluate_model(model, X_test_new, y_test_new, sns.color_palette("Greens"), output_dir, f"{model_name}_new")
#         print(f"{model_name} Accuracy on new dataset: {accuracy}")

def evaluate_model(model, X_test, y_test, colormap, output_dir, model_name):
    y_pred = model.predict(X_test)
    cm = pd.DataFrame(confusion_matrix(y_test, y_pred, normalize='true')*100)
    sns.heatmap(cm, annot=True, cmap=colormap)
    # Adding titles and labels
    plt.title(f'Confusion Matrix for {model_name}')
    plt.xlabel('Predicted Label')
    plt.ylabel('True Label')
    plt.savefig(os.path.join(output_dir, f'confusion_matrix_{model_name}.png'))
    plt.clf()  # Clear the current figure
    accuracy = accuracy_score(y_test, y_pred)
    return {
        "model": model_name,
        "accuracy": accuracy,
        "confusion_matrix": cm
    }

def test_on_new_dataset(test_data_dir, test_file_name, models, output_dir):
    # Load and preprocess test dataset
    test_processor = DataProcessor(test_data_dir, test_file_name)
    test_processor.default_preprocess()
    X_test_new = test_processor.df.iloc[:, 0:-1]
    y_test_new = test_processor.df.iloc[:, -1]

    results = []
    for model_name, model in models.items():
        model_results = evaluate_model(model, X_test_new, y_test_new, sns.color_palette("Greens"), output_dir, f"{model_name}_new")
        results.append(model_results)

    # Convert results to a DataFrame for better visualization and analysis
    results_df = pd.DataFrame(results)
    return results_df

# Main execution
input_dir = '/home/ubuntu/Project7008/data/Combined'
output_dir = '/home/ubuntu/Project7008/data/Results'
file_name = 'train_combined.csv'

# Create output directory
create_output_directory(output_dir)

# Data processing
processor = DataProcessor(input_dir, file_name)
processor.default_preprocess()

# Splitting data
X = processor.df.iloc[:, 0:-1]
y = processor.df.iloc[:, -1]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=0)

# Training models
RF, DT, LR = train_models(X_train, y_train)

# Evaluating and saving results
colormap_reds = sns.color_palette("Reds")
colormap_blues = sns.color_palette("Blues")

accuracy_RF = evaluate_model(RF, X_test, y_test, colormap_reds, output_dir, "RF")
accuracy_DT = evaluate_model(DT, X_test, y_test, colormap_reds, output_dir, "DT")
accuracy_LR = evaluate_model(LR, X_test, y_test, colormap_reds, output_dir, "LR")

# Print accuracy scores
print(f"Random Forest Accuracy: {accuracy_RF}")
print(f"Decision Tree Accuracy: {accuracy_DT}")
print(f"Logistic Regression Accuracy: {accuracy_LR}")


# Main execution - continued from previous script

# Assuming new dataset details
new_test_data_dir = '/home/ubuntu/Project7008/data/Combined'
new_test_file_name = 'test_combined.csv'

# Dictionary of trained models
trained_models = {'RF': RF, 'DT': DT, 'LR': LR}

# Testing on new dataset and getting results
test_results = test_on_new_dataset(new_test_data_dir, new_test_file_name, trained_models, output_dir)
print(test_results)

# Optional: Save the results DataFrame to a CSV file
test_results.to_csv(os.path.join(output_dir, 'test_results_summary.csv'), index=False)