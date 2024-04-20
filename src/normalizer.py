import pandas as pd

# Load data
bea_df = pd.read_csv('./data/db/BEA.csv', encoding='latin1') #Important to set the codec to latin1 to READ and utf-8 to WRITE for BEA
dimensions_df = pd.read_csv('./data/db/DIMENSIONS.csv', encoding='latin1') 

# Create new DataFrames with the desired column names and order
bea_merged = pd.DataFrame(columns=[f'BEA_{col}' for col in bea_df.columns] + [f'DIM_{col}' for col in dimensions_df.columns])
dimensions_merged = pd.DataFrame(columns=[f'BEA_{col}' for col in bea_df.columns] + [f'DIM_{col}' for col in dimensions_df.columns])

# Merge original datasets into the new DataFrames, filling missing fields with empty values
bea_merged = pd.merge(bea_merged, bea_df, left_index=True, right_index=True, how='outer')
dimensions_merged = pd.merge(dimensions_merged, dimensions_df, left_index=True, right_index=True, how='outer')

# Copy data from original columns to new columns
for col in bea_df.columns:
    bea_merged[f'BEA_{col}'] = bea_merged[col]
    bea_merged.drop(columns=col, inplace=True)

for col in dimensions_df.columns:
    dimensions_merged[f'DIM_{col}'] = dimensions_merged[col]
    dimensions_merged.drop(columns=col, inplace=True)

# Export the modified datasets
bea_merged.to_csv('./data/bea_normalized.csv', index=False, encoding='utf-8')
dimensions_merged.to_csv('./data/dimensions_normalized.csv', index=False , encoding='utf-8')