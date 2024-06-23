#!/usr/bin/env python
# coding: utf-8

# In[13]:


import sqlite3
import pandas as pd


# In[14]:


con = sqlite3.connect("proj6_readings.sqlite")


# In[15]:


df = pd.read_sql("SELECT count(*) from readings;", con)
df


# In[ ]:





# In[16]:


#EXERCISE 1


# In[17]:


result = pd.read_sql("SELECT COUNT(DISTINCT detector_id) as detector_count FROM readings;", con)
result
result.to_pickle("proj6_ex01_detector_no.pkl")


# In[18]:


#EXERCISE 2


# In[19]:


df = pd.read_sql("SELECT  * from readings LIMIT 2;", con)
df


# In[20]:


query = """
SELECT 
    detector_id, 
    COUNT(count) as measurement_count, 
    MIN(starttime) as min_starttime, 
    MAX(starttime) as max_starttime
FROM readings 
GROUP BY detector_id;
"""
result = pd.read_sql(query, con)
result
result.to_pickle("proj6_ex02_detector_stat.pkl")


# In[21]:


#EXERCISE 3


# In[22]:


query = """
SELECT 
    detector_id, 
    count, 
    LAG(count) OVER (PARTITION BY detector_id ORDER BY starttime) as prev_count
FROM readings
WHERE detector_id = 146
LIMIT 500;
"""
result = pd.read_sql(query, con)
result
result.to_pickle("proj6_ex03_detector_146_lag.pkl")


# In[28]:


query = """
SELECT 
    detector_id, 
    count, 
    SUM(count) OVER (PARTITION BY detector_id ORDER BY starttime ROWS BETWEEN CURRENT ROW AND 10 FOLLOWING) as window_sum
FROM readings
WHERE detector_id = 146
LIMIT 500;
"""
result = pd.read_sql(query, con)
result



# In[12]:


result = pd.read_sql(query, con)
result.to_pickle("proj6_ex04_detector_146_sum.pkl")


# In[ ]:


con.close()

