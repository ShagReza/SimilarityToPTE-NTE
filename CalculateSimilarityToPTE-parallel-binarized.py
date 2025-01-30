#-------------------------------------------------------------------------------
# Import necessary libraries
import pandas as pd
import numpy as np
from rdkit import DataStructs
from joblib import Parallel, delayed

#-------------------------------------------------------------------------------
# Load the WDR91 file (first 1000 rows, only 'Label' and 'ECFP4' columns)
wdr91_path = r'.\SimilarityQuestion\Label_Column.tsv'
wdr91_Label = pd.read_csv(wdr91_path, sep='\t', usecols=['Label'])

wdr91_path = r'.\SimilarityQuestion\ECFP4_Column.tsv'
wdr91_df = pd.read_csv(wdr91_path, sep='\t', usecols=['ECFP4'])

#-------------------------------------------------------------------------------
# Load the Nomination file (only 'ECFP4' column)
nomination_path = r".\SimilarityQuestion\ECFP4_Nominations_SMILES.xlsx"
try:
    nomination_df = pd.read_excel(nomination_path, usecols=['ECFP4'])
except FileNotFoundError:
    raise FileNotFoundError("Nomination file not found. Please provide the correct path.")
except ValueError as e:
    raise ValueError(f"Error: {str(e)}. Check if the specified columns exist in the Nomination file.")

#-------------------------------------------------------------------------------
# Function to calculate Tanimoto similarity for binary fingerprints
def tanimoto_similarity(fp1, fp2):
    """Calculates Tanimoto similarity using logical operations on binary arrays."""
    intersection = np.logical_and(fp1, fp2).sum()
    union = np.logical_or(fp1, fp2).sum()
    return intersection / union if union != 0 else 0

#-------------------------------------------------------------------------------
# Convert fingerprint strings to binary arrays
def convert_and_binarize_fp(fp_str, threshold=1):
    """Convert a fingerprint string to a binary array, binarizing values based on a threshold."""
    fp_array = np.array([int(x) for x in fp_str.split(',')])
    return (fp_array >= threshold).astype(int)

# Apply conversion and binarization to both dataframes
wdr91_fps = wdr91_df['ECFP4'].apply(convert_and_binarize_fp).values
nomination_fps = nomination_df['ECFP4'].apply(convert_and_binarize_fp).values

#-------------------------------------------------------------------------------
# Parallel computation of the similarity matrix
def compute_similarity_row(wdr91_fp, nomination_fps):
    """Compute a row of the similarity matrix."""
    return [tanimoto_similarity(wdr91_fp, nomination_fp) for nomination_fp in nomination_fps]

# Use joblib to parallelize row-wise similarity computation
similarity_matrix = Parallel(n_jobs=-1, backend='loky')(
    delayed(compute_similarity_row)(wdr91_fp, nomination_fps) for wdr91_fp in wdr91_fps
)

# Convert the result to a NumPy array
similarity_matrix = np.array(similarity_matrix)

#-------------------------------------------------------------------------------
# Create a DataFrame for the output
output_df = pd.DataFrame(similarity_matrix, columns=[f"Nomination_{j}" for j in range(len(nomination_df))])
output_df['Label'] = wdr91_Label

# Save the output to a CSV file
output_path = r'.\SimilarityQuestion\Similarity_Output.csv'
output_df.to_csv(output_path, index=False)

print(f"Similarity matrix saved to: {output_path}")

#-------------------------------------------------------------------------------
# Create a DataFrame with maximum similarity and corresponding Label
max_similarity_df = pd.DataFrame({
    'Maximum Similarity': similarity_matrix.max(axis=1),
    'Label': wdr91_Label['Label']
})

# Save the new DataFrame to an Excel file
max_similarity_output_path = r'.\SimilarityQuestion\Max_Similarity_Output.xlsx'
max_similarity_df.to_excel(max_similarity_output_path, index=False)

print(f"Max similarity data saved to: {max_similarity_output_path}")
#-------------------------------------------------------------------------------
