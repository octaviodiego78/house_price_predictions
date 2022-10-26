# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 22:47:36 2022

@author: octav
"""



import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import pandas as pd
import os
import numpy as np
import datetime
from selenium.webdriver.common.by import By


def getPages(n):
    '''
    

    Parameters
    ----------
    n : int
        number of pages to scrap.

    Returns
    -------
    links : list
        links of all the pages so to scrap the info of each one .

    '''
    
    links = []
    for i in range(1,n+1): 
        try:
            #https://www.vivanuncios.com.mx/s-casas-en-venta/zapopan/v1c1293l14828p{}
            link = 'https://www.vivanuncios.com.mx/s-casas-en-venta/zapopan/page-{}/v1c1293l14828p{}?sort=dt&order=asc'.format(str(i),str(i))
            links.append(link)
        
        except Exception as e:
            print(e)
            
        
    return links
        

def getLinks(page_links):
    '''
    GETS THE INDIVIDUAL HREF FROM ALL ELEMENTS OF AN SPECIFIC GRID

    Parameters
    ----------
    page_links : list
        links of all the pages to scrap.

    Returns
    -------
    house_links : list
        all individual house links .

    '''
    
    house_links = []
    page_n = 1
    for page_link in page_links:
        
        page = requests.get(page_link)
        print('Getting links from page:', str(page_n),'....')
        page_n += 1
        time.sleep(3)
        soup = BeautifulSoup(page.text, 'html.parser')
        
        div1 = soup.findAll('div', {'class': 'viewport-contents'})
         
        for div in div1:
            div2 = div.findAll('div', {'class': ['tileV2 REAdTileV2 promoted listView', 'tileV2 REAdTileV2 regular listView']})
            
            for div in div2:
                div3 = div.findAll('div', {'class': 'tile-desc one-liner'})
                
                for div in div3:
                    a_class = div.findAll('a', {'class': 'href-link tile-title-text'})
                    
                    for a in a_class:
                        link = 'https://www.vivanuncios.com.mx' + a['href']
                        #print(link)
                        house_links.append(link)
        
    
    return house_links
        




def getInfo(links):
    '''
    

    Parameters
    ----------
    link : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    '''
    
    options = webdriver.ChromeOptions();
    options.add_argument('headless');
    driver = webdriver.Chrome(executable_path='{}\{}'.format(os.getcwd(),'chromedriver.exe'),options=options)
    
    #Info to fill
    titles = []
    prices = []
    creation_dates = []
    views = []
    sellers = []
    
    bedrooms = []
    baths = []
    half_baths = []
    garages = []
    mts = []
    seller_types = []
    descriptions = []
    locations = []
    links2 = []
    
    
    
    count = 1
    for link in links:
        
        print('Scraping link {}...'.format(count))
        links2.append(link)
        
        try:
            #Opening the link
            page = requests.get(link)
            time.sleep(5)
            soup = BeautifulSoup(page.text, 'html.parser')
            
            
            try:
            
                prop_names = soup.findAll('span', {'class': 'pri-props-name'})           
                names = [name.text for name in prop_names]
                
                prop_values = soup.findAll('span', {'class': 'pri-props-value'})
                values = [name.text for name in prop_values]
                
                
                
                # --------------- Bedrooms -------------
                
                if 'Recámara(s):' in names:
                    bedrooms.append(str(values[names.index('Recámara(s):')]))
                    
                else:
                    bedrooms.append(np.nan)
                    
    
                # --------------- Baths -------------
                
                if 'Baños:' in names:
                    baths.append(str(values[names.index('Baños:')]))
                    
                else:
                    baths.append(np.nan)
                          
                                     
    
                # --------------- Half Baths -------------
                
                if 'Medio Baños:' in names:
                    half_baths.append(str(values[names.index('Medio Baños:')]))
                    
                else:
                    half_baths.append(np.nan)
    
                          
                
                #----------------Garages-----------------
                
                if 'Garage:' in names:
                    garages.append(str(values[names.index('Garage:')]))
                    
                else:
                    garages.append(np.nan)
                
                    
                                     
                # --------------- mts -------------
                
                if 'Terreno:' in names:
                    mts.append(str(values[names.index('Terreno:')]))
                    
                else:
                    mts.append(np.nan)
                    
                    
                # --------------- Seller Type  -------------
                
                if 'Vendedor(a):' in names:
                    seller_types.append(values[names.index('Vendedor(a):')])
                    
                else:
                    seller_types.append(np.nan)
                
                
                
                # ------------------- TITLE  ----------------------------------------------------------------
                try:
                    title = soup.find('h1', {'class': 'item-title'}).find('div', {'class': 'title'}).text
                    titles.append(title)
                    
                except:
                    titles.append(np.nan)
                    
                
                # ------------------- PRICE  ----------------------------------------------------------------
                try:
                    price = soup.find('h3', {'class': 'social-border'}).find('span', {'class': 'ad-price'}).text
                    prices.append(price)
                    
                except:
                    prices.append(np.nan)
                  
                    
                # ------------------- CREATION DATE  --------------------------------------------------------
                    
                try:
                    date = soup.find('div', {'class': 'last-post'}).find('span', {'class': 'creation-date'}).text
                    creation_dates.append(date)
                    
                except:
                    creation_dates.append(np.nan)  
                    
                
                # ------------------- VIEWS  ------------------------------------------------------------------
                    
                try:
                    view = soup.find('div', {'class': 'last-post'}).find('span', {'class': 'view-count'}).text
                    views.append(view)
                    
                except:
                    views.append(np.nan)  
                    
                    
                # ------------------- SELLER  ------------------------------------------------------------------
                    
                try:
                    seller = soup.find('div', {'class': 'profile'}).find('div', {'class': 'profile-username'}).text
                    sellers.append(seller)
                    
                except:
                    sellers.append(np.nan) 
                    
                
                # ------------------- DESCRIPTION  ------------------------------------------------------------------
                  
                #Dinamic scrapping
                try:
                    driver.get(link)
                    description = driver.find_element(By.CLASS_NAME, 'description-content').text
                    descriptions.append(description)
                    
                except:
                    descriptions.append(np.nan) 
                    
                # ------------------- Locations  ------------------------------------------------------------------
                
                #Dinamic scrapping
                try:
                    
                    driver.get(link)
                    location = driver.find_element(By.CLASS_NAME,"location-name").text
                    locations.append(location)
                
                    
                except:
                    locations.append(np.nan) 
                   
                
            except Exception as e:
                 print('Prop {} had the following error: {}'.format(count, e))
                
                
                
        except Exception as e:
             print('Link {} had the following error: {}'.format(count, e))
             
        count += 1
    
    df = pd.DataFrame({'title' : titles,
                                'price' : prices,
                                'date' : creation_dates,
                                'views' : views,
                                'seller' : sellers,
                                'bedrooms' : bedrooms,
                                'baths' : baths,
                                'half_baths' : half_baths,
                                'garages' : garages,
                                'mts' : mts,
                                'seller_type' : seller_types,
                                'descriptions':descriptions,
                                'location':locations,
                                'link':links2}, 
                                columns=['title','price', 'date','views',
                                         'seller','bedrooms','baths',
                                         'half_baths','garages','mts','seller_type','descriptions','location','link'])
    
    print(df.info())
    
    return df



def main():
    
    links = getLinks(getPages(30))
    df = getInfo(links)
    df.to_csv('df.csv')    

start = datetime.datetime.now()
main()
end = datetime.datetime.now()


try:
    
    print((end-start).seconds)
    
except:
    pass

