#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


import json


# In[3]:


#EXERCISE 1


# In[4]:


def generate_json(df):
    missing_values_count = df.isnull().sum()

    total_rows = len(df)

    missing_values_percentage = missing_values_count / total_rows

    data_types = df.dtypes.apply(lambda x: 'int' if x == 'int64' else ('float' if x == 'float64' else 'other'))

    data = []
    for column in df.columns:
        data.append({
            'name': column,
            'missing_values': missing_values_percentage.get(column, 0.0),
            'data_type': data_types[column]
        })

    json_file = 'proj1_ex01_fields.json'
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"JSON file '{json_file}' has been generated successfully.")


# In[5]:


df=pd.read_csv('proj1_ex01.csv')


# In[6]:


generate_json(df)


# In[7]:


#EXERCISE 2


# In[8]:


df.head()


# In[9]:


print(df["two"].transpose().describe().to_dict())


# In[10]:


print(df["five"].transpose().describe().to_dict())


# In[11]:


def value_statistics(df):
    data = {}
    for column in df.columns:
        data[column] = df[column].describe().to_dict()

    json_file = 'proj1_ex02_stats.json'
    with open(json_file, 'w') as file:
        json.dump(data, file, indent=4)

    print(f"JSON file '{json_file}' has been generated successfully.")


# In[12]:


value_statistics(df)


# In[13]:


#EXERCISE 3


# In[14]:


import re


# In[15]:


cleaned_columns = [re.sub(r'[^A-Za-z0-9_ ]', '', col).lower().replace(' ', '_') for col in df.columns]

new_df = df.copy()
new_df.columns = cleaned_columns

new_df.to_csv('proj1_ex3_columns.csv', index=False)



# In[16]:


#EXERCISE 4


# In[17]:


#EXCEL
df.to_excel('proj1_ex04_excel.xlsx', index=False)

#JSON
df.to_json('proj1_ex04_json.json', orient='records')

#PICKLE
df.to_pickle('proj1_ex04_pickle.pkl')


# In[18]:


#EXERCISE 5


# In[19]:


dataframe = pd.read_pickle("proj1_ex05.pkl")

selected_columns = dataframe.iloc[:, 1:3]

filtered_data = selected_columns[selected_columns.index.str.startswith('v')]

filtered_data = filtered_data.fillna("")

filtered_data.to_markdown("proj1_ex05_table.md", index=True)

print("Filtered DataFrame has been saved as a markdown table.")


# In[20]:


#EXERCISE 6


# In[21]:


def read_json(filename: str) -> dict: 
  
    try: 
        with open(filename, "r") as f: 
            data = json.loads(f.read()) 
    except: 
        raise Exception(f"Reading {filename} file encountered an error") 
  
    return data 
  
def normalize_json(data: list) -> dict: 
    new_data = {}
    for idx, item in enumerate(data):
        for key, value in item.items():
            if isinstance(value, dict):
                for k, v in value.items():
                    new_data[f"{key}_{k}_{idx}"] = v
            else:
                new_data[f"{key}_{idx}"] = value
    return new_data
 
  
  
 
data = read_json(filename="proj1_ex06.json") 
 
new_data = normalize_json(data=data) 
  
print("New dict:", new_data, "\n") 
  
dataframe = pd.DataFrame(new_data, index=[0]) 

dataframe.to_pickle("proj1_ex06_pickle.pkl") 


# In[ ]:




