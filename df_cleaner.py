# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 23:04:52 2022

@author: octav
"""

import os 
import pandas as pd
from datetime import datetime,timedelta
import numpy as np

df = pd.read_csv('{}\{}.csv'.format(os.getcwd(),'df'),encoding='latin-1')




def acronym(string):
    '''
    

    Makes an upper acronym from a string
    ----------
    string : str
        DESCRIPTION.

    Returns
    -------
    s : str
        DESCRIPTION.

    '''
    
    
    w = [word[0].upper() for word in string.split()]
    s = ''
    for letter in w:
        s += letter

    return s
    


def date_converter(string,formating=False):
    
    split = string.split()
    
    if 'un' in split:       
        
        if 'año' in split:
            days = 365
        
        elif 'mes' in split:
            days = 30
        
        else:
            days =1
             
    else:
        
        if 'años' in split:
            days = int(split[1])*365
            
        elif 'meses' in split:
            days = int(split[1])*30
            
        else:
            days = int(split[1])
     
    date_posted = datetime.now()  - timedelta(days=days)

    
    return date_posted



def views_getter(string):
    
    views = int(string.split()[0])
    return views


# ----------------------- Main -----------------------------------------------
    

def cleaner(df) : 
    
    
    #Managing null values
    df = df[df.title.notnull()]   
    df = df[df.date.notnull()]
    df = df[df.price.notnull()]
    df = df[df.location.notnull()]
    
    
    #Replacing np.nan values
   
    fills = {'bedrooms':0,'baths':0,'half_baths':0,'garages':0}
    

    df.fillna(value=fills,inplace=True)

    df['half_baths'] = df['half_baths'].astype('string')


    #Views wouldnt be used in regression and we dow want to inpact the views info
    df['views'].replace(np.nan,0,inplace=True)
    
    #Same with seller    
    df['id'] = df['title'].apply(acronym)
    df['id'] = df.id.str.replace('(','')
    df['id'] = df.id.str.replace('\d+', '')
    df.drop(['title'], axis=1,inplace=True)
    
    
    
    #Giving format to price
    
    def price_cleaner(string):
        
        if 'USD' in string.upper():
            string = string.replace('$','')
            string = string.replace(',','')
            string = string.replace('USD','')
            
            return int(string)*20
        
        else:
            string = string.replace('$','')
            string = string.replace(',','')
            string = string.replace('USD','')
            
            return int(string)
     
    
    df['price'] = df['price'].apply(price_cleaner)
    
    #Calculating date posted
    df['date'] = df['date'].apply(date_converter)

    
    #Calculating amount of days posted 
    df['days_published'] = (datetime.now() - df['date'])
    df['days_published'] = df['days_published'].dt.days
    
    
    #Getting views 
    df['views'] = df['views'].apply(views_getter)

    
    #Getting bedrooms
    df['bedrooms'] = df['bedrooms'].str.replace('+', '').fillna(df['bedrooms']).astype(float)
    
    
    #Formatting baths    

    df['baths']=df['baths'].str.replace('+', '').fillna(df['baths']).astype(float)    
    df['half_baths'] = df['half_baths'].str.replace('+', '').fillna(df['half_baths']).astype(float)   
    df['baths'] = df['baths'] + (df['half_baths'] / 2)   
    df['baths'] = df['baths'].replace(0.0,df['baths'].mean()).round(1)
        
    df.drop(['half_baths'], axis=1,inplace=True)
    
   
    #Getting garages   
    df['garages'] = df['garages'].str.replace('+', '').fillna(df['garages']).astype(float)
    
    
    
    
    df = df[df.mts.notnull()]
    df['mts'] = df.mts.str.replace('m2', '').str.strip().astype('int32')
    
    
    #price_per_meter   
    df['price_per_mt'] = df['price'] / df['mts']
    
    
    


    
    
    return df



cleaner(df).to_csv('cleaned_df.csv')



