#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Importing Libraries
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Handling the Dataset. 

Inpath= "C:/Users/kelli/Documents/DCU/Y4/Mt413-Data Mining/Group Assignment Data/" 
column_types = {'neighbourhood_group': str}
BnB_Df=pd.read_csv(Inpath+"US_BNB_2023.csv", delimiter=","
                   ,header=0, index_col=0, dtype = column_types)
BnB_Df


# In[2]:


#Describe the dataset 
print(BnB_Df.head())
print(BnB_Df.tail())
print(BnB_Df.shape)


# In[3]:


BnB_Df.describe(include="all")


# In[4]:


#Handling missing / Nan values
(BnB_Df.isna().sum(axis=0)) 
print(BnB_Df.isna().sum(axis=0)/len(BnB_Df))


# In[5]:


BnB_Df["neighbourhood_group"].fillna(value="Not Specified", inplace=True)
(BnB_Df.isna().sum(axis=0)/len(BnB_Df))


# In[6]:


BnB_Df.dropna(subset=["reviews_per_month","last_review","name","host_name"], inplace=True)
BnB_Df


# In[7]:


#Checking for duplicated rows, deleting them while keeping the first instance. 
print("There are " + str(BnB_Df.duplicated().sum()) + " duplicated Rows")

#return duplicated rows
duplicated_rows = BnB_Df[BnB_Df.duplicated(keep=False)]
print(duplicated_rows)

#remove duplicated rows. 
BnB_Df_unique=BnB_Df.drop_duplicates(keep="first")
BnB_Df_unique


# In[8]:


#Investigating categorical data. 
BnB_Df_unique.describe(include="object")


# In[9]:


#Investigating Numerical data. 
BnB_Df_unique.describe(include=np.number)


# In[10]:


# Looking at the difference between the Mean, 75th percentile and the Max values of the "minimum_nights" variable.
#We identified that we should remove values above 365 (the number of days in a year). 
BnB_Df_unique= BnB_Df_unique[BnB_Df_unique["minimum_nights"]<=365]
BnB_Df_unique.describe(include=np.number)


# In[11]:


# Investigating "reviews_per_month" feature. The max value seemed high as there are only 
#30 days in a month and there is a 14 day window for completing a review. 

#Examining through percentiles.
percentiles = [25, 50, 75, 90, 95]  

percentiles.extend([i/10 for i in range(990, 1000, 1)] + [100])

# Calculate the percentiles of the 'price' column
price_percentiles = np.percentile(BnB_Df['reviews_per_month'], percentiles)

# Print the calculated percentiles
for percentile, value in zip(percentiles, price_percentiles):
    print(f'{percentile}th Percentile: {value:.2f}')


# In[12]:


#It is clear from the percentiles that 101.42 is an outlier so we will 
#keep values less than or equal to 13.22
BnB_Df_unique= BnB_Df_unique[BnB_Df_unique["reviews_per_month"]<=13.23]
BnB_Df_unique.describe(include=np.number)


# In[13]:


BnB_Df_unique_numeric=BnB_Df_unique[["latitude","longitude","price","minimum_nights"
                                     ,"number_of_reviews","reviews_per_month"
                                     ,"availability_365","number_of_reviews_ltm"]]
BnB_Df_unique_numeric


# In[14]:


#Choosing z-score or IQR method for smoothing out large data.

mean_BnB_Df_unique_numeric=BnB_Df_unique_numeric["price"].mean()
std_BnB_Df_unique_numeric=BnB_Df_unique_numeric["price"].std()
Upper_bound=mean_BnB_Df_unique_numeric+3*std_BnB_Df_unique_numeric
Lower_bound=mean_BnB_Df_unique_numeric-3*std_BnB_Df_unique_numeric
print("Upper Bound")
print(Upper_bound)
print("Lower Bound")
print(Lower_bound)

Z_Out_BnB_Df_unique_numeric=BnB_Df_unique_numeric[(BnB_Df_unique_numeric["price"]>Lower_bound) 
                                   & (BnB_Df_unique_numeric["price"]<Upper_bound)]
Z_Out_BnB_Df_unique_numeric


# In[15]:


#Identify the upper and lower bounds using the IQR method for the ‘price’ variable
Q1=BnB_Df_unique_numeric["price"].quantile(.25)
Q3=BnB_Df_unique_numeric["price"].quantile(.75)
print("Q1=", Q1)
print("Q3= ", Q3)

IQR=Q3-Q1
print("IQR= ", IQR)

Lwr_bound=Q1-1.5*IQR
Upr_bound=Q3+1.5*IQR
print("Lower Bound= ",Lwr_bound)
print("Upper Bound= ",Upr_bound)

IQR_Out_BnB_Df_unique_numeric=BnB_Df_unique_numeric[(BnB_Df_unique_numeric["price"]>Lwr_bound) &
                                                    (BnB_Df_unique_numeric["price"]<Upr_bound)]
IQR_Out_BnB_Df_unique_numeric


# In[16]:


#Investigating into which method would remove more data for further understanding of the data. 
print('Number of point removed with the z-score method: ' + str(len(BnB_Df_unique_numeric) - len(Z_Out_BnB_Df_unique_numeric)))
print('Number of point removed with the IQR method: ' + str(len(BnB_Df_unique_numeric) - len(IQR_Out_BnB_Df_unique_numeric)))


# In[17]:


# Investigate if the dataset is Normally distributed in order to choose a method. 

#Calculate skewness for all columns
skewness = BnB_Df_unique_numeric.skew()
print("Skewness:")
print(skewness)

# Calculate kurtosis for all columns
kurtosis = BnB_Df_unique_numeric.kurtosis()
print("\nKurtosis:")
print(kurtosis)


# In[18]:


# Display the min and max values in IQR_Out_BnB_Df_unique_numeric.
print('     Min values')
pd.set_option('display.float_format', '{:.0f}'.format)
print(IQR_Out_BnB_Df_unique_numeric.min())
print('     Max values')
pd.set_option('display.float_format', '{:.0f}'.format)
print(IQR_Out_BnB_Df_unique_numeric.max())


# In[19]:


#As the majority of the data is not normally distributed and our 
#data contains extreme outliers in the price column we will use the IQR to smooth out the data. 


# In[20]:


# Smooth out the large values in noOutlrIqrDf using the logarithm (np.log) and display the min and max
IQR_Out_BnB_Df_unique_numeric_log = IQR_Out_BnB_Df_unique_numeric.apply(np.log)
IQR_Out_BnB_Df_unique_numeric_log


# In[21]:


print('     Min values')
print(IQR_Out_BnB_Df_unique_numeric_log.min())
print('     Max values')
print(IQR_Out_BnB_Df_unique_numeric_log.max())

# Negative infinity returned due to zero values. 
# Nan returned due to negative values. 
# After consideration all of the values we are content to accept the log function. 


# In[22]:


# Displaying the distribution of the "price" after smoothing using the log transformation.
plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.histplot(IQR_Out_BnB_Df_unique_numeric['price'], color="r", bins=30)
plt.title('Distribution of Price (Before Log Transformation)')
plt.xlabel("Price")
plt.subplot(1, 2, 2)
sns.histplot(IQR_Out_BnB_Df_unique_numeric_log['price'], color="g", bins=30)
plt.title('Distribution of Price (After Log Transformation)')
plt.xlabel("Price")
plt.show()


# In[23]:


# Now it can be seen that all of the data is within the acceptable bounds of -7 and 7. 
IQR_Out_BnB_Df_unique_numeric.describe()


# In[24]:


numerical_data=IQR_Out_BnB_Df_unique_numeric

merged_BnB_Df = pd.merge(numerical_data, BnB_Df_unique[["neighbourhood","room_type","city"]], left_index=True, right_index=True)

# Display the merged dataset
print(merged_BnB_Df)
merged_BnB_Df


# In[25]:


merged_BnB_Df.to_csv(Inpath + 'US_BNB_2023_Cleaned.csv', index=True)

