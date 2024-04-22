#!/usr/bin/env python
# coding: utf-8

# In[1]:


#############################################################
#                     Feature Engineering                   #
#############################################################


# In[2]:


import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

#Handling the Dataset. 

Inpath= "C:/Users/kelli/Documents/DCU/Y4/Mt413-Data Mining/Group Assignment Data/" 
column_types = {'neighbourhood_group': str}
merged_BnB_Df=pd.read_csv(Inpath+"US_BNB_2023_Cleaned.csv", delimiter=","
                   ,header=0, index_col=0, dtype = column_types)
merged_BnB_Df


# In[3]:


#Creating two new columns in BnB_Df_unique called "avg_price_neigh" and "avg_price_city" which will contain 
#the average price per neighbourbood and city. 

avg_price_neigh = merged_BnB_Df.groupby('neighbourhood')['price'].transform('mean')
merged_BnB_Df['avg_price_neigh'] = merged_BnB_Df['price'] / avg_price_neigh
merged_BnB_Df['avg_price_neigh']



# In[9]:


#Creating a new column in BnB_Df_unique called "avg_price_city" which will contain the average price per city. 
avg_price_neigh = merged_BnB_Df.groupby('city')['price'].transform('mean')
merged_BnB_Df['avg_price_city'] = merged_BnB_Df['price'] / avg_price_neigh
merged_BnB_Df['avg_price_city']


# In[5]:


#Using One-Hot Encoding on the nominal variable "room_type". 
merged_BnB_Df = pd.get_dummies(merged_BnB_Df, columns=['room_type'], prefix='property_type')


# In[8]:


#Assuming that properties with more reviews have higher satisfaction rates as if the reviews 
#were negative they would not get as many bookings and therefore not have a high number of reviews. 
#create a feature called "customer_satisfaction"

merged_BnB_Df["customer_satisfaction"]=merged_BnB_Df["number_of_reviews"]/merged_BnB_Df["availability_365"]

