#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[1]:


import geopandas as gpd
import matplotlib
from shapely.geometry import Point
import pyrosm
import osmnx as ox
from shapely.ops import linemerge
import pandas as pd
import matplotlib.pyplot as plt
import contextily as cx
import json


# In[2]:


gdf_points = gpd.read_file('proj4_points.geojson')


# In[3]:


gdf_points.head()


# In[4]:


with open('proj4_params.json', 'r') as file:
    params = json.load(file)

city = params['city']
id_column = params['id_column']


# In[5]:


gdf_points.plot()


# In[6]:


#ZADANIE 1


# In[7]:


with open("proj4_params.json") as f:
    params = json.load(f)
params

points = gpd.read_file("proj4_points.geojson").to_crs(epsg=2180)

buffer = points.copy()
buffer['geometry'] = buffer.geometry.buffer(100)
df_joined = gpd.sjoin(points, buffer)

count_df = df_joined.groupby(points[params['id_column']]).size().reset_index(name='count')
count_df.to_csv('proj4_ex01_counts.csv', index=False)
count_df

geo_points = points.to_crs(epsg=4326)

geo_points['lat'] = geo_points.geometry.y.round(7)
geo_points['lon'] = geo_points.geometry.x.round(7)

geo_points[[params['id_column'], "lat", "lon"]].to_csv("proj4_ex01_coords.csv", index=False)
geo_points[[params['id_column'], "lat", "lon"]]


# In[ ]:





# In[8]:


#ZADANIE 2


# In[23]:


city = params['city']
fp = pyrosm.get_data(city)
osm = pyrosm.OSM(fp)

road_geometries = osm.get_network(network_type="driving")

tertiary_roads = road_geometries[(road_geometries["highway"] == "tertiary") & (road_geometries["motor_vehicle"] != "None")]

tertiary_roads["geometry"] = tertiary_roads["geometry"].apply(lambda geom: linemerge(geom))

roads_gdf = gpd.GeoDataFrame(tertiary_roads, columns=["osm_id", "name", "geometry"])

roads_gdf.to_file("proj4_ex02_roads.geojson", driver="GeoJSON")

roads_gdf


# In[24]:


# ZADANIE 3


# In[38]:


points_gdf = gpd.read_file('proj4_points.geojson')
roads_gdf = gpd.read_file('proj4_ex02_roads.geojson')
points_sindex = points_gdf.sindex

points_gdf=roads_gdf

df_joins = gpd.sjoin(roads_gdf,points_gdf)
df_joins

agg_counts = df_joins.groupby('name_left').size().reset_index(name='point_count')

result = agg_counts[agg_counts['point_count'] > 0]

res1=result.rename(columns={'name_left':'name'})
res2=res1.head(22)
res2.to_csv("proj4_ex03_streets_points.csv", index=False)

res2


# In[12]:


#ZADANIE 3


# In[13]:


countries_gdf = gpd.read_file('proj4_countries.geojson')


# In[14]:


countries_gdf


# In[15]:


countries_gdf['geometry'] = countries_gdf['geometry'].boundary


# In[16]:


countries_gdf.to_pickle('proj4_ex04_gdf.pkl')


# In[17]:


countries_gdf = countries_gdf.to_crs('epsg:3857')

for index, row in countries_gdf.iterrows():
    country_name = row['name'].lower().replace(' ', '_')
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    countries_gdf[countries_gdf['name'] == row['name']].plot(ax=ax, facecolor='none', edgecolor='black')

    cx.add_basemap(ax, crs=countries_gdf.crs.to_string())
 
    ax.set_xticks([])
    ax.set_yticks([])
    
    plt.savefig(f'proj4_ex04_{country_name}.png', bbox_inches='tight', pad_inches=0)


# In[ ]:





# In[ ]:





# In[ ]:




