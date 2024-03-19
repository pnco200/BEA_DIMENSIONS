import pandas as pd
import Levenshtein as lev

#Const
beaPath = "./data/bea_normalized.csv"
dimensionsPath = "./data/dimensions_normalized.csv"

#I Use the normalized datasets for simplicity in the merging process
bea_df = pd.read_csv(beaPath, encoding='utf-8')
dimensions_df = pd.read_csv(dimensionsPath, encoding='utf-8')

#I create the data frame with these values to avoid panda converting integers into floating point numbers
merged_df = pd.DataFrame({
    'A': [1.0, 2.0, 3.0],
    'B': [4.0, float('nan'), 6.0],  # Contains NaN
    'C': [7.0, float('inf'), 9.0]    # Contains infinity
})
i = 0
#Function where i apply Levishtain distance for title similarity, default value is set to 80% similarity
def is_similar(title1, title2, threshold=0.80):
    global i
    distance = lev.distance(title1.lower(), title2.lower()) #Lowercas to avoid levenshtein case sensitivity swap
    max_length = max(len(title1), len(title2)) 
    similarity_ratio = 1 - distance / max_length
    if(similarity_ratio >= threshold):
        i+=1
        print(distance, " ", similarity_ratio, "\n", title1,"\n", title2, "\n", i)
        
    return similarity_ratio >= threshold

# Get records that are only in normalized DIMENSIONS
dimensions_only_df = dimensions_df[~dimensions_df['DIM_Title'].apply(lambda x: any(is_similar(x, title) for title in bea_df['BEA_title']))]


#Concatenate normalized bea with the unique records of normalized dimensions
merged_df = pd.concat([bea_df, dimensions_only_df])


# Find columns with float dtype
int_columns = merged_df.select_dtypes(include=['float64']).columns

# Replace non-finite values with 0
merged_df[int_columns] = merged_df[int_columns].fillna(0)

# Convert columns to integers
merged_df[int_columns] = merged_df[int_columns].astype(int)

merged_df = merged_df.replace(0, pd.NA)

# Export the final dataset
merged_df.to_csv('./data/merged.csv', index=False , encoding='utf-8')