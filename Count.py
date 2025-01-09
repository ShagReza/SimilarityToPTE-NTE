import pandas as pd

# File path
file_path = r"D:\0000-UHN\SimilarityQuestion\Similarity_Output.csv"

# Load the CSV file
data = pd.read_csv(file_path)

# Initialize a list to store results
results = []

# Process each Nomination column
for col in [f"Nomination_{i}" for i in range(0, 50)]:
    if col in data.columns:
        # Filter data by label
        label_0 = data[data['Label'] == 0]
        label_1 = data[data['Label'] == 1]
        
        # Calculate counts and percentages for Label = 0
        label_0_count = len(label_0)
        label_0_above_0_7 = (label_0[col] > 0.7).sum()
        label_0_below_0_4 = (label_0[col] < 0.4).sum()
        label_0_above_0_7_pct = (label_0_above_0_7 / label_0_count) * 100 if label_0_count > 0 else 0
        label_0_below_0_4_pct = (label_0_below_0_4 / label_0_count) * 100 if label_0_count > 0 else 0

        # Calculate counts and percentages for Label = 1
        label_1_count = len(label_1)
        label_1_above_0_7 = (label_1[col] > 0.7).sum()
        label_1_below_0_4 = (label_1[col] < 0.4).sum()
        label_1_above_0_7_pct = (label_1_above_0_7 / label_1_count) * 100 if label_1_count > 0 else 0
        label_1_below_0_4_pct = (label_1_below_0_4 / label_1_count) * 100 if label_1_count > 0 else 0

        # Append results
        results.append({
            "Column": col,
            "Label 0 - Above 0.7 (Count)": label_0_above_0_7,
            "Label 0 - Above 0.7 (%)": label_0_above_0_7_pct,
            "Label 0 - Below 0.4 (Count)": label_0_below_0_4,
            "Label 0 - Below 0.4 (%)": label_0_below_0_4_pct,
            "Label 1 - Above 0.7 (Count)": label_1_above_0_7,
            "Label 1 - Above 0.7 (%)": label_1_above_0_7_pct,
            "Label 1 - Below 0.4 (Count)": label_1_below_0_4,
            "Label 1 - Below 0.4 (%)": label_1_below_0_4_pct
        })

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save results to an Excel file
output_file_path = r"D:\0000-UHN\SimilarityQuestion\Similarity_Output_Analysis_With_Percentages.xlsx"
results_df.to_excel(output_file_path, index=False)

output_file_path
