import pandas as pd
import Levenshtein as lev
import warnings
import datetime

#I use this to avoid the warning of the future version of pandas
warnings.simplefilter(action='ignore', category=FutureWarning)
#Const
beaPath = "./data/bea_normalized.csv"
dimensionsPath = "./data/dimensions_normalized.csv"

#Golbals
indicesUnique = []

indicesDuplicated = []

#I Use the normalized datasets for simplicity in the merging process
bea_df = pd.read_csv(beaPath, encoding='utf-8')
dimensions_df = pd.read_csv(dimensionsPath, encoding='utf-8')

#I create the data frame with these values to avoid panda converting integers into floating point numbers
merged_df = pd.DataFrame({
    'A': [1.0, 2.0, 3.0],
    'B': [4.0, float('nan'), 6.0],  # Contains NaN
    'C': [7.0, float('inf'), 9.0]    # Contains infinity
})

#Function that calculates the similarity between two strings using the Levenshtein distance
def levensthein_distance_ratio(str1, str2):
    if pd.isnull(str1) or pd.isnull(str2):
        return 0.0
    distance = lev.distance(str1.lower(), str2.lower())
    max_length = max(len(str1), len(str2))
    return 1 - distance / max_length

#Function where i apply Levishtain distance for title similarity, default value is set to 80% similarity and 20% for authors
def is_similar(title1, title2, auth1, auth2, year1, year2, threshold_title=0.8, threshold_authors=0.2):
    try:
        year1 = int(year1)
        year2 = int(year2)
    except:
        #Tengo que hacer este try catch porque en BEA el registro numero 1154 esta corrupto
        return False
    similarity_ratio_title = levensthein_distance_ratio(title1, title2)
    similarity_ratio_authors = levensthein_distance_ratio(auth1, auth2)
    if(year1 == year2):
        if similarity_ratio_title >= threshold_title:
            if similarity_ratio_authors >= threshold_authors:
                return True
    return False
        
def findIndexes():
    duplicatedCounter = 0
    uniqueCounter = 0
    for index, row in dimensions_df.iterrows():
        if not any(is_similar(row['DIM_Title_dim'], title, row['DIM_Authors_dim'], auth, row['DIM_PubYear_dim'], year) for title, auth, year in zip(bea_df['BEA_title'], bea_df['BEA_authors'], bea_df['BEA_year'])):
            uniqueCounter += 1
            indicesUnique.append(index)
        else:
            duplicatedCounter += 1
            indicesDuplicated.append(index)
    print("Ammount of duplicated records: ", duplicatedCounter)
    print("Ammount of unique records: ", uniqueCounter)
    #write the number of unique and duplicated records to a log file
    with open("log.txt", "w") as file:
        file.write("Ammount of duplicated records: " + str(duplicatedCounter) + "\n")
        file.write("Ammount of unique records: " + str(uniqueCounter) + "\n")
    #I create both the dataframes for the unique and repeated records
    dimensions_only_df = dimensions_df.loc[indicesUnique]
    dimensions_repeated_df = dimensions_df.loc[indicesDuplicated]
    
    #
    fillDuplicated(dimensions_repeated_df)
    finish(dimensions_only_df)

#Modifies the bea dataframe to add the dimensions values on the repeated records
def fillDuplicated(dimensions_repeated_df):
    for index, row in dimensions_repeated_df.iterrows():
        for index2, row2 in bea_df.iterrows():
            if is_similar(row['DIM_Title_dim'], row2['BEA_title'], row['DIM_Authors_dim'], row2['BEA_authors'], row['DIM_PubYear_dim'], row2['BEA_year']):
                #DIM_Rank,DIM_Authors,DIM_PubYear,DIM_Title,DIM_reference,DIM_Abstract,DIM_Funding,DIM_MeSH_terms,DIM_Publication_Type,DIM_Corresponding_Authors,DIM_Research_Organizations_._standardized,DIM_Country_of_standardized_research_organization,DIM_Funder,DIM_Funder_Group,DIM_Funder_Country,DIM_Times_cited,DIM_Recent_citations,DIM_RCR,DIM_Fields_of_Research_.ANZSRC_2020.,DIM_RCDC_Categories,DIM_HRCS_HC_Categories,DIM_HRCS_RAC_Categories,DIM_CSO_Categories
                bea_df.at[index2, "DIM_Rank_dim"] = row["DIM_Rank_dim"]
                bea_df.at[index2, "DIM_Authors_dim"] = row["DIM_Authors_dim"]
                bea_df.at[index2, "DIM_Title_dim"] = row["DIM_Title_dim"]
                bea_df.at[index2, "DIM_PubYear_dim"] = row["DIM_PubYear_dim"]
                bea_df.at[index2, "DIM_Abstract_dim"] = row["DIM_Abstract_dim"]
                bea_df.at[index2, "DIM_Funding_dim"] = row["DIM_Funding_dim"]
                bea_df.at[index2, "DIM_MeSH_terms_dim"] = row["DIM_MeSH_terms_dim"]
                #bea_df.at[index2, "DIM_Publication_Type"] = row["DIM_Publication_Type"]
                bea_df.at[index2, "DIM_Corresponding_Authors_dim"] = row["DIM_Corresponding_Authors_dim"]
                bea_df.at[index2, "DIM_Research_Organizations_._standardized_dim"] = row["DIM_Research_Organizations_._standardized_dim"]
                bea_df.at[index2, "DIM_Country_of_standardized_research_organization_dim"] = row["DIM_Country_of_standardized_research_organization_dim"]
                bea_df.at[index2, "DIM_Funder_dim"] = row["DIM_Funder_dim"]
                bea_df.at[index2, "DIM_Funder_Group_dim"] = row["DIM_Funder_Group_dim"]
                bea_df.at[index2, "DIM_Funder_Country_dim"] = row["DIM_Funder_Country_dim"]
                bea_df.at[index2, "DIM_Times_cited_dim"] = row["DIM_Times_cited_dim"]
                bea_df.at[index2, "DIM_Recent_citations_dim"] = row["DIM_Recent_citations_dim"]
                bea_df.at[index2, "DIM_RCR_dim"] = row["DIM_RCR_dim"]
                bea_df.at[index2, "DIM_Fields_of_Research_.ANZSRC_2020._dim"] = row["DIM_Fields_of_Research_.ANZSRC_2020._dim"]
                bea_df.at[index2, "DIM_RCDC_Categories_dim"] = row["DIM_RCDC_Categories_dim"]
                bea_df.at[index2, "DIM_HRCS_HC_Categories_dim"] = row["DIM_HRCS_HC_Categories_dim"]
                bea_df.at[index2, "DIM_HRCS_RAC_Categories_dim"] = row["DIM_HRCS_RAC_Categories_dim"]
                bea_df.at[index2, "DIM_CSO_Categories_dim"] = row["DIM_CSO_Categories_dim"]
                bea_df.at[index2, "DIM_FCR_dim"] = row["DIM_FCR_dim"]
                bea_df.at[index2, "DIM_Pagination_dim"] = row["DIM_Pagination_dim"]
                bea_df.at[index2, "DIM_Issue_dim"] = row["DIM_Issue_dim"]
                bea_df.at[index2, "DIM_Volume_dim"] = row["DIM_Volume_dim"]
                bea_df.at[index2, "DIM_Source_title_dim"] = row["DIM_Source_title_dim"]
    return True

#Concatenates bea with the unique records of dimensions and exports the final dataset
def finish(dimensions_only_df):
    #Concatenate normalized bea with the unique records of normalized dimensions
    merged_df = pd.concat([bea_df, dimensions_only_df])


    # Find columns with float dtype
    int_columns = merged_df.select_dtypes(include=['float64']).columns

    # Replace non-finite values with 0
    merged_df[int_columns] = merged_df[int_columns].fillna(0)

    # Convert columns to integers
    merged_df[int_columns] = merged_df[int_columns].astype(int)

    merged_df = merged_df.replace(0, pd.NA)
    # Get the current date and time
    now = datetime.datetime.now()

    # Format the date and time as a string
    date_time_str = now.strftime("%d-%m-%Y_%H%M")

    # Construct the file name with the date and time
    file_name = f"./data/merged_{date_time_str}.csv"

    # Save the DataFrame to the file
    merged_df.to_csv(file_name, index=False, encoding='utf-8')
#Main function, initializes the process
findIndexes()