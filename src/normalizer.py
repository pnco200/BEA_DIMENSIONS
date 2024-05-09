import pandas as pd
from langdetect import detect, LangDetectException

# Load data
bea_df = pd.read_csv('./data/db/BEA.csv', encoding='latin1') #Important to set the codec to latin1 to READ and utf-8 to WRITE for BEA
dimensions_df = pd.read_csv('./data/db/DIMENSIONS.csv', encoding='latin1') 

# Create new DataFrames with the desired column names and order
bea_merged = pd.DataFrame(columns=[f'BEA_{col}' for col in bea_df.columns] + [f'DIM_{col}' for col in dimensions_df.columns])
dimensions_merged = pd.DataFrame(columns=[f'BEA_{col}' for col in bea_df.columns] + [f'DIM_{col}' for col in dimensions_df.columns])

# Merge original datasets into the new DataFrames, filling missing fields with empty values
bea_merged = pd.merge(bea_merged, bea_df, left_index=True, right_index=True, how='outer')
dimensions_merged = pd.merge(dimensions_merged, dimensions_df, left_index=True, right_index=True, how='outer')

def detect_lang(text):
    try:
        return detect(str(text))
    except LangDetectException:
        return "Unknown"

# Copy data from original columns to new columns
for col in bea_df.columns:
    bea_merged[f'BEA_{col}'] = bea_merged[col]
    bea_merged.drop(columns=col, inplace=True)

bea_merged['lang'] = bea_merged['BEA_title'].apply(detect_lang)


for col in dimensions_df.columns:
    dimensions_merged[f'DIM_{col}'] = dimensions_merged[col]
    dimensions_merged.drop(columns=col, inplace=True)

dimensions_merged['lang'] = dimensions_merged['DIM_Title_dim'].apply(detect_lang)

# Export the modified datasets
bea_merged.to_csv('./data/bea_normalized.csv', index=False, encoding='utf-8')
dimensions_merged.to_csv('./data/dimensions_normalized.csv', index=False , encoding='utf-8')