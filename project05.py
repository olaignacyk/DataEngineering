#!/usr/bin/env python
# coding: utf-8

# In[1]:


import json
import pandas as pd
import re


# In[2]:


with open('proj5_params.json', 'r') as file:
    proj5_params = json.load(file)
print(proj5_params)


# In[3]:


#EX1


# In[4]:


df=pd.read_csv('proj5_timeseries.csv')
df


# In[5]:


for name in df.columns:
  rename = re.sub(r'[^a-zA-Z]', '_', name).lower()
  df.rename(columns={name:rename}, inplace=True)


# In[6]:


df['date'] = pd.to_datetime(df['date'], format='mixed')
df.set_index('date', inplace=True)


# In[7]:


df


# In[8]:


df = df.asfreq(proj5_params['original_frequency'])

df.to_pickle('proj5_ex01.pkl')

print(df)


# In[9]:


#EX 2


# In[10]:


df2 = df.asfreq(proj5_params['target_frequency'])


# In[11]:


df2.to_pickle('proj5_ex02.pkl')


# In[12]:


#EX 3


# In[13]:


periods = proj5_params['downsample_periods']
units = proj5_params['downsample_units']

df_down = df.resample(str(periods) + units).sum(min_count=periods)

df_down.to_pickle('proj5_ex03.pkl')
print(df_down)


# In[14]:


#EX 4


# In[15]:


rule = str(proj5_params['upsample_periods']) + proj5_params['upsample_units']
df_upsampled = df.resample(rule).asfreq().interpolate(method=proj5_params['interpolation'], order=proj5_params['interpolation_order'])

original_freq = pd.Timedelta(df.index.freq).total_seconds()
upsampled_freq = pd.Timedelta(df_upsampled.index.freq).total_seconds()
ratio = upsampled_freq  / original_freq
df_upsampled *= ratio

df_upsampled.to_pickle('proj5_ex04.pkl')

print(df_upsampled)


# In[16]:


#EX 5


# In[17]:


df = pd.read_pickle('proj5_sensors.pkl')


# In[18]:


df.index = pd.to_datetime(df.index)


# In[19]:


df['device_id'].unique()


# In[20]:


sensors_periods = proj5_params['sensors_periods']
sensors_units = proj5_params['sensors_units']

df = df.pivot(columns=['device_id'], values='value')


# In[21]:


new_index = pd.date_range(df.index.round(f'{sensors_periods}{sensors_units}').min(), 
df.index.round(f'{sensors_periods}{sensors_units}').max(), freq=f'{sensors_periods}{sensors_units}')


# In[22]:


df.reindex(new_index)
df = df.reindex(new_index.union(df.index)).interpolate()
df = df.reindex(new_index)
df = df.dropna()
df.to_pickle('proj5_ex05.pkl')


# In[23]:


print(df)


# In[ ]:




