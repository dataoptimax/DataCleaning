#!/usr/bin/env python
# coding: utf-8

# # Remove Duplicate Real Estate Listings in Levallois-Perret

# ## Introduction

# This project focuses on removing duplicate real estate listings in Levallois-Perret. The dataset at hand consists of current real estate listings for sale in Levallois-Perret. The objective is to identify and group together listings that pertain to the same property. By eliminating duplicates, the project aims to improve search efficiency and provide accurate statistics by effectively removing duplicate listings.

# ## Importing Libraries and Data

# In[21]:


import pandas as pd
import matplotlib.pyplot as plt
import time


# In[22]:


# Start the timer
start_time = time.time()


# In[23]:


# Read the Excel file into a DataFrame
df = pd.read_excel('C:/Users/Admin/Downloads/Dataset - Ads _ Levallois-Perret - 2019-08.xlsx')


# ## Data Exploration

# In[24]:


# Display the first few rows of the dataset
#print("Sample records:")
#print(df.head())


# In[25]:


# Check the shape of the dataset (number of rows, number of columns)
print("Dataset shape:")
print(df.shape)


# In[26]:


# Get summary statistics of the dataset
#print("Summary statistics:")
#print(df.describe())


# In[27]:


# Check the data types of each column
#print("Data types:")
#print(df.dtypes)


# In[28]:


# Check for missing values in the dataset
print("Missing values:")
print(df.isnull().sum())


# In[29]:


# Identify and extract into a dataframe duplicate rows based on 'DESCRIPTION'
duplicate_rows1 = df.duplicated(subset='DESCRIPTION', keep=False)
df_duplicates1 = df[duplicate_rows1]

# Remove rows with empty values in 'DESCRIPTION'
df_duplicates1 = df_duplicates1.dropna(subset=['DESCRIPTION'])

#sort to group duplicates together
df_duplicates1.sort_values('DESCRIPTION')


# I faced challenges while finding duplicates due to missing values, but I discovered a reliable subset of columns for accurate identification and removal. Different subsets should be considered for future analyses, adapting to the dataset's characteristics for optimal results.

# In[30]:


# Identify and extract into a dataframe duplicate rows based on specified columns
columns = ['MARKETING_TYPE', 'PRICE', 'PRICE_M2', 'RENTAL_EXPENSES', 'FEES_INCLUDED', 'OCCUPIED', 'DEALER_NAME', 'DEALER_TYPE']
duplicate_rows2 = df.duplicated(subset=columns, keep=False)
df_duplicates2 = df[duplicate_rows2]

# Remove rows with empty values in all subset columns
df_duplicates2 = df_duplicates2.dropna(subset=columns, how='all')

#sort to group duplicates together
df_duplicates2.sort_values(columns)


# ## Identifying Duplicate Records

# In[31]:


def assign_ids(dataframe, columns, column_name):
    id_counter = 1
    id_map = {}  # Dictionary to store row values and their corresponding IDs
    
    for index, row in dataframe.iterrows():
        # Extract the values from the specified columns and convert them to a tuple
        row_values = tuple(row[columns].values)
        
        if row_values in id_map:
            # If the row values already exist in the dictionary, assign the corresponding ID
            row_id = id_map[row_values]
        else:
            # If the row values are encountered for the first time, assign a new ID
            row_id = id_counter
            id_map[row_values] = row_id
            id_counter += 1
        
        # Assign the ID to the specified column of the current row
        dataframe.loc[index, column_name] = row_id
    
    # Convert the specified column to integers
    dataframe[column_name] = dataframe[column_name].astype(int)
    
    # Move the specified column to the first place
    dataframe.insert(0, column_name, dataframe.pop(column_name))
    
    # Sort the DataFrame by the specified column
    dataframe = dataframe.sort_values(column_name)
    
    return dataframe


# ## Identifying, Concatenating and Removing Duplicate Records identified through the column description

# In[32]:


#assign the same value in the column ID_DUPLICATES to the rows with the same description
df_duplicates = assign_ids(df, ['DESCRIPTION'],'ID_DUPLICATES')


# In[33]:


#concatenate the string columns that are different for the duplicates
string_columns=['ID', 'URL', 'CRAWL_SOURCE', 'IMAGES','PUBLICATION_START_DATE','LAST_CRAWL_DATE']
df_concat=df_duplicates.groupby('ID_DUPLICATES')[string_columns].agg(lambda x: ' '.join(x))

df_concat


# In[34]:


# Drop duplicates in 'df_duplicates'
df_duplicates = df_duplicates.drop_duplicates(subset='ID_DUPLICATES')
df_duplicates

#Set ID_DUPLICATES as index
df_duplicates.set_index('ID_DUPLICATES', inplace=True)


# In[35]:


# Updating values in df_duplicates with values from df_concat
df_duplicates.update(df_concat)

df_duplicates


# ## Identifying, Concatenating and Removing Duplicate Records identified through the list columns

# In[36]:


# Drop the 'ID_DUPLICATES' column
df_duplicates.reset_index(drop=True, inplace=True)

#assign the same value to the rows with the same values for the given columns
df_duplicates = assign_ids(df_duplicates, columns,'ID_DUPLICATES')

#concatenate the string columns that are different for the duplicates
string_columns=['ID', 'URL', 'DESCRIPTION', 'CRAWL_SOURCE', 'IMAGES','PUBLICATION_START_DATE','LAST_CRAWL_DATE']
df_concat=df_duplicates.groupby('ID_DUPLICATES')[string_columns].agg(lambda x: ' '.join(x))

# Drop duplicates in 'df_duplicates'
df_duplicates = df_duplicates.drop_duplicates(subset='ID_DUPLICATES')
df_duplicates

#Set ID_DUPLICATES as index
df_duplicates.set_index('ID_DUPLICATES', inplace=True)

# Updating values in df_duplicates with values from df_concat
df_duplicates.update(df_concat)

df_duplicates


# ## Verification and Result Analysis

# In[37]:


# End the timer
end_time = time.time()

# Calculate the elapsed time
elapsed_time = end_time - start_time

# Print the elapsed time
print("Elapsed time: ", elapsed_time, " seconds")


# In[42]:


#number of duplicates removed
num_duplicates = len(df) - len(df_duplicates)
print("Number of duplicates removed : ",num_duplicates)


# In[44]:


#Calculate the percentage of duplicates removed
percentage_removed = round((num_duplicates / len(df)) * 100)
print(f"Percentage of duplicates removed: {percentage_removed}%")


# In[38]:


# Create a bar plot
plt.bar(['Duplicates', 'Remaining'], [num_duplicates, len(df_duplicates)])

# Add labels and title
plt.xlabel('Data')
plt.ylabel('Count')
plt.title('Duplicate Removal Result')

# Display the plot
plt.show()


# ## Conclusion

# After applying this flow, a total of 313 duplicates were successfully removed from the DataFrame within approximately 10 seconds. This efficient approach to data cleaning and refinement ensures the accuracy and quality of subsequent analyses or operations performed on the dataset.
# 
# Challenges were encountered during the duplicate identification process due to missing values. However, accurate identification was achieved using the "description" column and a selected subset of columns.To optimize results and extend the methodology for future analyses, it is recommended to apply the duplicate identification process to additional relevant columns. This approach offers flexibility and scalability in handling duplicates across various data subsets as the flow can be easily adapted to address duplicate values in different parts of the dataset.
# 
# Furthermore, the concatenation of duplicates guarantees that no information is lost during the deduplication process. This consolidation of data from different sources or listings ensures a comprehensive representation of the dataset, enabling a more thorough and enriched analysis.
# 
# Overall, this process provides a reliable solution for identifying and removing duplicates, promoting data integrity, and enabling more robust data analysis and manipulation.
