# -*- coding: utf-8 -*-
"""
Created on Wed Jan  8 13:40:14 2025

@author: shagh
"""

import pandas as pd

wdr91_path = r'D:\0000-UHN\03-DataAndCodes\Data\HitGen\WDR91.tsv\WDR91.tsv'
output_path = r'D:\0000-UHN\SimilarityQuestion\ECFP4_Column.tsv'
Label_path = r'D:\0000-UHN\SimilarityQuestion\Label_Column.tsv'

try:
    # Read only the 'ECFP4' column
    ecfp4_df = pd.read_csv(wdr91_path, sep='\t', usecols=['ECFP4'])
    Label_df = pd.read_csv(wdr91_path, sep='\t', usecols=['Label'])
    
    # Save the column to a new TSV file
    ecfp4_df.to_csv(output_path, sep='\t', index=False)
    Label_df.to_csv(Label_path, sep='\t', index=False)
    print(f"'ECFP4' column saved to: {output_path}")
except FileNotFoundError:
    print("File not found. Please provide the correct path.")
except ValueError as e:
    print(f"Error: {str(e)}. Check if the specified column exists in the file.")
