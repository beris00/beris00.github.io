#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler 

Inpath= "C:/Users/erisb/Downloads/" 
column_types = {'neighbourhood_group': str}
merged_BnB_Df=pd.read_csv(Inpath+"US_BNB_2023_Cleaned(EB).csv", delimiter=","
                   ,header=0, index_col=0, dtype = column_types)
merged_BnB_Df


# In[3]:


avg_price_neigh = merged_BnB_Df.groupby('neighbourhood')['price'].transform('mean')
merged_BnB_Df['avg_price_neigh'] = merged_BnB_Df['price'] / avg_price_neigh
merged_BnB_Df['avg_price_neigh']


# In[4]:


avg_price_city = merged_BnB_Df.groupby('city')['price'].transform('mean')
merged_BnB_Df['avg_price_city'] = merged_BnB_Df['price'] / avg_price_city
merged_BnB_Df['avg_price_city']


# In[5]:


merged_BnB_Df["customer_satisfaction"]=merged_BnB_Df["number_of_reviews"]/merged_BnB_Df["availability_365"]
merged_BnB_Df


# In[9]:


#I removed all catagorical columns to allow for ploting

merged_BnB_Df_cluster=merged_BnB_Df.drop(["neighbourhood","city","room_type","customer_satisfaction"],axis=1)
merged_BnB_Df_cluster


# In[10]:


#We tested to ensure that we could plot the information without errors before commencing K-Means
plt.plot(merged_BnB_Df_cluster)
plt.show()


# In[11]:


inertia = []
for k in range(1, 11):
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(merged_BnB_Df_cluster)
    inertia.append(kmeans.inertia_)
    
plt.plot(range(1, 11), inertia, marker='o')
plt.title('Elbow Method for Optimal k')
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Distance')
plt.show()


# In[ ]:





# In[17]:


#Based on the elbow method we chose an optimal value for k. Our graph is quite curved and an arguement could be made for either 2 or 4
#We chose 2
optimal_k = 2
kmeans = KMeans(n_clusters=optimal_k, random_state=42)
merged_BnB_Df['Cluster'] = kmeans.fit_predict(merged_BnB_Df_cluster)

#We added a new column to our dataframe called "Cluster"
print(merged_BnB_Df['Cluster'].value_counts())


# In[18]:


merged_BnB_Df


# In[ ]:




