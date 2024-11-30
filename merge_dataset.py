import pandas as pd

# Read the CSV files
epi_df = pd.read_csv('epi_r.csv')
food_cal_df = pd.read_csv('nutrients_csvfile.csv')

# Convert numeric columns to float in both dataframes
numeric_columns = ['calories', 'protein', 'fat']
for col in numeric_columns:
    epi_df[col] = pd.to_numeric(epi_df[col], errors='coerce')
    food_cal_df[col] = pd.to_numeric(food_cal_df[col], errors='coerce')

# Merge the dataframes on common columns
merged_df = pd.merge(epi_df, food_cal_df, 
                    on=['title', 'calories', 'protein', 'fat'],
                    how='outer')
merged_df = merged_df.drop_duplicates()

# Sort the merged dataframe alphabetically by title
merged_df = merged_df.sort_values(by='title', ascending=True)

# Save the merged dataset to a new CSV file
merged_df.to_csv('merged_dataset.csv', index=False)

