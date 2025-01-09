#-------------------------------------------------------------------------------
# Import necessary libraries
import pandas as pd
import numpy as np

#-------------------------------------------------------------------------------
# Load the WDR91 file (first 1000 rows, only 'Label' and 'ECFP4' columns)
wdr91_path = r'D:\0000-UHN\SimilarityQuestion\Label_Column.tsv'
wdr91_Label = pd.read_csv(wdr91_path, sep='\t', usecols=['Label'])
wdr91_path = r'D:\0000-UHN\SimilarityQuestion\ECFP4_Column.tsv'
wdr91_df = pd.read_csv(wdr91_path, sep='\t', usecols=['ECFP4'])
#-------------------------------------------------------------------------------
# Load the Nomination file (only 'ECFP4' column)
nomination_path = r"D:\0000-UHN\SimilarityQuestion\BinaryECFP4_Nominations_SMILES.xlsx"
try:
    nomination_df = pd.read_excel(nomination_path, usecols=['ECFP4'])
except FileNotFoundError:
    raise FileNotFoundError("Nomination file not found. Please provide the correct path.")
except ValueError as e:
    raise ValueError(f"Error: {str(e)}. Check if the specified columns exist in the Nomination file.")

#-------------------------------------------------------------------------------
# Calculate Tanimoto similarity
def tanimoto_similarity(fp1_str, fp2_str):
    # Convert comma-separated strings to numpy arrays
    try:
        fp1 = np.array([int(x) for x in fp1_str.split(',')])
        fp2 = np.array([int(x) for x in fp2_str.split(',')])
    except:
        return 0  # Return 0 similarity if conversion fails

    # Calculate Tanimoto similarity
    intersection = np.logical_and(fp1, fp2).sum()
    union = np.logical_or(fp1, fp2).sum()
    return intersection / union if union != 0 else 0

#-------------------------------------------------------------------------------
# Create an empty similarity matrix

similarity_matrix = np.zeros((len(wdr91_df), len(nomination_df)))

# Populate the similarity matrix
for i, wdr91_fp_str in enumerate(wdr91_df['ECFP4']):
    print(i)
    for j, nomination_fp_str in enumerate(nomination_df['ECFP4']):
        similarity_matrix[i, j] = tanimoto_similarity(wdr91_fp_str, nomination_fp_str)

#-------------------------------------------------------------------------------
# Create a DataFrame for the output
output_df = pd.DataFrame(similarity_matrix, columns=[f"Nomination_{j}" for j in range(len(nomination_df))])
output_df['Label'] = wdr91_Label

# Save the output to a CSV or TSV file
output_path = r'D:\0000-UHN\SimilarityQuestion\Similarity_Output.csv'
output_df.to_csv(output_path, index=False)

print(f"Similarity matrix saved to: {output_path}")


# Create a new DataFrame with maximum similarity and corresponding Label
max_similarity_df = pd.DataFrame({
    'Maximum Similarity': similarity_matrix.max(axis=1),
    'Label': wdr91_Label['Label']
})

# Save the new DataFrame to an Excel file
max_similarity_output_path = r'D:\0000-UHN\SimilarityQuestion\Max_Similarity_Output.xlsx'
max_similarity_df.to_excel(max_similarity_output_path, index=False)

print(f"Max similarity data saved to: {max_similarity_output_path}")
#-------------------------------------------------------------------------------
