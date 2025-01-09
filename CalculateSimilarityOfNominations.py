
    
    
#----------------------------------------------------------------------------
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fingerprints import HitGenBinaryECFP4, HitGenFCFP6  # Import the HitGenBinaryECFP4 fingerprint class
from sklearn.metrics.pairwise import cosine_similarity

# Define the path to the Excel file
Nomination_path = r"D:\0000-UHN\SimilarityQuestion\Nominations_SMILES.xlsx"

# Read the Excel file into a DataFrame
data = pd.read_excel(Nomination_path)

# Check if the SMILES column exists in the DataFrame
if 'SMILES' not in data.columns:
    raise ValueError("The Excel file does not contain a 'SMILES' column.")

# Extract the SMILES column
smiles_list = data['SMILES'].tolist()

# Instantiate the HitGenBinaryECFP4 class
#binary_ecfp4_generator = HitGenBinaryFCFP4()
fcfp6_generator = HitGenFCFP6()

# Generate fingerprints for each SMILES string (resulting in a 50x2048 array)
#fingerprint_array = binary_ecfp4_generator.generate_fps(smis=smiles_list)
fingerprint_array = fcfp6_generator.generate_fps(smis=smiles_list)

# Calculate Tanimoto similarity matrix
def tanimoto_similarity(fp1, fp2):
    intersection = np.logical_and(fp1, fp2).sum()
    union = np.logical_or(fp1, fp2).sum()
    return intersection / union if union != 0 else 0

similarity_matrix = np.zeros((len(fingerprint_array), len(fingerprint_array)))
for i in range(len(fingerprint_array)):
    for j in range(len(fingerprint_array)):
        similarity_matrix[i, j] = tanimoto_similarity(fingerprint_array[i], fingerprint_array[j])

# Visualize the similarity matrix
plt.figure(figsize=(10, 8))
plt.imshow(similarity_matrix, cmap='viridis', interpolation='nearest')
plt.colorbar(label='Tanimoto Similarity')
plt.title('Tanimoto Similarity Matrix')
plt.xlabel('Fingerprint Index')
plt.ylabel('Fingerprint Index')
plt.savefig(r"D:\0000-UHN\SimilarityQuestion\\Tanimoto_Similarity_Matrix.png")
plt.show()

# Convert each 2048-length fingerprint into a comma-separated string
fingerprint_strings = [','.join(map(str, fp)) for fp in fingerprint_array]

# Add the fingerprints as a new column to the DataFrame
#data['BinaryECFP4'] = fingerprint_strings
data['FCFP6'] = fingerprint_strings

# Save the updated DataFrame back to an Excel file (optional)
output_path = r"D:\0000-UHN\SimilarityQuestion\FCFP6_Nominations_SMILES.xlsx"
data.to_excel(output_path, index=False)

print(f"Fingerprints added successfully. Updated file saved at: {output_path}")

#----------------------------------------------------------------------------



