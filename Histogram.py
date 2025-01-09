# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 14:42:54 2025

@author: shagh
"""
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt

# Load the Excel file
file_path = r"D:\0000-UHN\SimilarityQuestion\Max_Similarity_Output.xlsx"
data = pd.read_excel(file_path)

# Check if the file has the required columns
if 'Maximum Similarity' in data.columns and 'Label' in data.columns:
    # Separate data based on Labels
    label_0_data = data[data['Label'] == 0]['Maximum Similarity']
    label_1_data = data[data['Label'] == 1]['Maximum Similarity']
    
    # Plot histogram for Label = 0
    plt.figure(figsize=(8, 6))
    plt.hist(label_0_data, bins=50, alpha=0.7, edgecolor='black')
    plt.title('Histogram of Maximum Similarity for Label = 0')
    plt.xlabel('Maximum Similarity')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

    # Plot histogram for Label = 1
    plt.figure(figsize=(8, 6))
    plt.hist(label_1_data, bins=50, alpha=0.7, edgecolor='black')
    plt.title('Histogram of Maximum Similarity for Label = 1')
    plt.xlabel('Maximum Similarity')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()
else:
    print("The required columns 'Maximum Similarity' and 'Labels' are not present in the file.")

#-----------------------------------------------------------------------------
