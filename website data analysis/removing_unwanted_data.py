import pandas as pd

file_path = "results.xlsx"
df = pd.read_excel(file_path)

exclude_columns = df.columns[:2]  # Exclude the first two columns

df = df.loc[~(df.loc[:, ~df.columns.isin(exclude_columns)] == 0).all(axis=1)]


output_file_path = "Output/OutputData.xlsx"
df.to_excel(output_file_path, index=False)

print("Rows with all 0 values (excluding first two columns) removed. Result saved to:", output_file_path)
