# -*- coding: utf-8 -*-
"""
Created on Sat Sep 24 15:09:52 2022

@author: octav
"""
import pandas as pd
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split



df = pd.read_csv('{}\{}.csv'.format(os.getcwd(),'cleaned_df'),encoding='latin-1')
df = df[df.location.notnull()].reset_index()

#Categorical variable codification
average = df.groupby('location')['price_per_mt'].mean()
sizes = df.groupby('location')['price_per_mt'].size()

df['average_price'] = df['location'].map(average)
df['houses_in_place'] = df['location'].map(sizes)

#Deleting outlier price rows

q = df.price.quantile([0.25,0.5,0.75])
iqr=q.loc[0.75]-q.loc[0.25] # Q3-Q1
df2 = df.loc[(df.price < (1.5*iqr + q.loc[0.75])) & (df.price > (q.loc[0.25] - 1.5*iqr ))].reset_index()




#normalization with min and max
    
df2['mts_reg'] = (df2['mts'] - df2['mts'].min()) / (df2['mts'].max() - df2['mts'].min())
df2['location_reg'] = (df2['average_price'] - df2['average_price'].min()) / (df2['average_price'].max() - df2['average_price'].min())



#train and test

x = df2[['bedrooms','baths','garages','mts_reg','location_reg']]
y = df2['price']

X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=39)


#Creating the model
lr = LinearRegression()
lr.fit(X_train,y_train)


#Getting scores
print('Scores')

print('Train')
print(lr.score(X_train,y_train))

print('Test')
print(lr.score(X_test,y_test))
print('')


df2['pred'] = lr.predict(x)
df2['diff'] = abs(abs(df2.pred)-abs(df2.price))
df2['error_percentage'] = abs((df2.pred - df2.price) / df2.price)


df2.to_csv('results.csv')
