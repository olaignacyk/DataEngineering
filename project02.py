#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import re


# In[2]:


separators = [';', ',', '|']
decimal = [',', '.']
flag = False

for separator in separators:
    for decimal_ in decimal:
        try:
            df = pd.read_csv("proj2_data.csv", sep=separator, decimal=decimal_)
            if len(df.columns) > 1 and len(df.select_dtypes(include=['float']).columns) > 0:
                df.to_pickle("proj2_ex01.pkl")
                flag = True
                break
        except Exception as e:
            print("Erorr")
    if flag==True:
        break

df


# In[3]:


df.head()


# In[4]:


df.to_pickle("proj2_ex01.pkl")


# In[5]:


df.info()


# In[6]:


#EXERCISE 2


# In[7]:


with open("proj2_scale.txt", 'r') as f:
    scale_value = {line.strip(): index + 1 for index, line in enumerate(f)} 

df_copy = df.copy()

for column in df_copy.columns:
    df_copy[column] = df_copy[column].map(scale_value).fillna(df_copy[column])

df_copy.to_pickle("proj2_ex02.pkl")


# In[8]:


df_copy


# In[9]:


#EXERCISE 3


# In[10]:


df_copy2 = df.copy()

for col in df_copy2.columns:
    if(set(df_copy2[col]).issubset(set(scale_value.keys()))):
        df_copy2[col] = pd.Categorical(df_copy2[col], categories=scale_value.keys())

        
df_copy2
df_copy2.info()


# In[11]:


df_copy2.to_pickle("proj2_ex03.pkl")


# In[12]:


#EXERCISE 4


# In[13]:


df_copy3=df.copy()


# In[14]:


df_copy3.head()


# In[15]:


extracted_data={}

pattern = r'[-]?\d+[\.,]?\d*'
columns_with_numeric_values = []

for column in df.select_dtypes(exclude=['number']):
    extracted_nums = []
    for val in df[column]:
        val_str = str(val.replace(',', '.'))
        match = re.search(pattern, val_str)
        if match:
            extracted_nums.append(float(match.group()))
        else:
            extracted_nums.append(None)
    if any(extracted_nums):
        extracted_data[column] = extracted_nums

extracted_df = pd.DataFrame(extracted_data)
extracted_df.to_pickle("proj2_ex04.pkl")

extracted_df


# In[16]:


#EXERCISE 5


# In[17]:


candidate_columns = []
for column in df.select_dtypes(include=['object']):
    if (df[column].nunique() <= 10 and                    
        df[column].str.islower().all() and                
        not df[column].isin(scale_value).any()):        
        candidate_columns.append(column)

for i,column in enumerate(candidate_columns):
    encoded_df = pd.get_dummies(df[column])
    encoded_df.to_pickle(f"proj2_ex05_{i+1}.pkl")


# In[ ]:





# In[ ]:




