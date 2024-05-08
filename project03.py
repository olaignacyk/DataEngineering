#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import csv
import json


# In[2]:


file_list = ['proj3_data1.json','proj3_data2.json','proj3_data3.json'] 
dfs=[]
for file in file_list:
    data = pd.read_json(file)
    dfs.append(data) 
df = pd.concat(dfs, ignore_index=True)


# In[3]:


df


# In[4]:


#ZADANIE 2.2


# In[5]:


results = []
for column in df:
    if df[column].isna().any():
        results.append((column, df[column].isna().sum()))
print(results)
results_df = pd.DataFrame(results)
results_df.to_csv('proj3_ex02_no_nulls.csv', header=False, index=False)


# In[6]:


#ZADANIE 2.3


# In[7]:


with open('proj3_params.json', 'r') as f:
    params = json.load(f)
params


# In[8]:


df['description'] = df[params['concat_columns']].apply(lambda x: ' '.join(x), axis=1)
df


# In[9]:


df.to_json('proj3_ex03_descriptions.json')


# In[10]:


#ZADANIE 2.4


# In[11]:


more_data=pd.read_json('proj3_more_data.json')
more_data


# In[12]:


new_df = df.merge(more_data, on=params['join_column'], how='left')
new_df.to_json('proj3_ex04_joined.json')


# In[13]:


new_df


# In[14]:


#ZADANIE 2.5


# In[15]:


def handle_nan(value):
    if pd.isna(value):
        return None
    return value
next_df=new_df


# In[16]:


for index, row in next_df.iterrows():
    description = row['description']
    row_without_description = row.drop('description')
    row_without_description = row_without_description.apply(handle_nan)
    filename = f'ex05_{description.lower().replace(" ", "_")}.json'
    with open(filename, 'w') as file:
        json.dump(row_without_description.to_dict(), file)


# In[17]:


for index, row in next_df.iterrows():
    description = row['description']
    row_without_description = row.drop('description')
    row_without_description = row_without_description.apply(handle_nan)
    for col in params['int_columns']:
        if col in row_without_description.index:
            row_without_description[col] = int(row_without_description[col]) if pd.notnull(row_without_description[col]) else None
    filename = f'proj3_ex05_int_{description.lower().replace(" ", "_")}.json'
    with open(filename, 'w') as file:
        json.dump(row_without_description.to_dict(), file)


# In[ ]:





# In[18]:


#ZADANIE 2.6


# In[19]:


aggregated_data = {}
for col_name, func in params['aggregations']:
    key = f"{func}_{col_name}"
    if func == 'min':
        aggregated_data[key] = new_df[col_name].min()
    elif func == 'max':
        aggregated_data[key] = new_df[col_name].max()
    elif func == 'mean':
        aggregated_data[key] = new_df[col_name].mean()


with open('proj3_ex06_aggregations.json', 'w') as json_file:
    json.dump(aggregated_data, json_file)


# In[20]:


#ZADANIE 2.7


# In[21]:


grouped = new_df.groupby(params['grouping_column'])
grouped_filtered = grouped.filter(lambda x: len(x) > 1)
mean_values_list = []
for group_name, group_data in grouped_filtered.groupby(params['grouping_column']):
    mean_values = group_data.select_dtypes(include='number').mean()
    mean_values.name = group_name
    mean_values_list.append(mean_values)

result_df = pd.concat(mean_values_list, axis=1).T

result_df.to_csv('proj3_ex07_groups.csv', header=True, index=True)


# In[ ]:





# In[22]:


#ZADANIE 2.8


# In[23]:


pivot_table_df = pd.pivot_table(new_df, 
                                index=params['pivot_index'],         
                                columns=params['pivot_columns'],      
                                values=params['pivot_values'],        
                                aggfunc='max').reset_index().rename_axis(None, axis=1)

# pivot_table_df.to_pickle('proj3_ex08_pivot.pkl')


# In[ ]:





# In[24]:


pivot_df=new_df.melt(id_vars=params['id_vars'])
pivot_df.to_csv('proj3_ex08_melt.csv',header=True,index=False)
pivot_df


# In[29]:


stat_df=pd.read_csv('proj3_statistics.csv')
stat_df


# In[30]:


index_column_name = stat_df.columns[0]
stat_df.set_index(index_column_name, inplace=True)

prefixes = stat_df.columns.str.split('_').str[0].unique().dropna()
suffixes = stat_df.columns.str.split('_').str[1].unique().dropna()

stat_df.rename(columns=lambda x: x.replace('_','').replace('.',''), inplace=True)


new_stat_df = pd.wide_to_long(stat_df.reset_index(), 
                              stubnames=prefixes, 
                              i=index_column_name, 
                              j='Year',  
                              suffix='\\w+').reset_index()

new_stat_df[index_column_name] = new_stat_df[index_column_name].apply(lambda x: f"'{x}'")

new_stat_df['Country_Year'] = new_stat_df.apply(lambda row: (row[index_column_name],row['Year']), axis=1)

new_stat_df.drop(columns=[index_column_name, 'Year'], inplace=True)
new_stat_df.set_index('Country_Year', inplace=True)
new_stat_df.index.name = None
new_stat_df


# In[31]:


new_stat_df.to_pickle('proj3_ex08_stats.pkl')


# In[ ]:





# In[ ]:




