# -*- coding: utf-8 -*-
"""
Created on Sun Jun 21 12:01:05 2020

@author: YIT
"""

import urllib.parse
import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

import selenium


# this script will allow user to use name
try:
    driver
except NameError:
    driver = webdriver.Chrome('C:/Users/YIT/chromedriver_win32/chromedriver.exe')
else:
    print("This file is called from another python script such that the variable 'driver' has been defined.")


driver.get('https://tools.morningstarthailand.com/th/stockquickrank/default.aspx?Site=th&LanguageId=en-TH/');
drop_down_num_page = driver.find_element_by_id("ctl00_ContentPlaceHolder1_msStockQuickrankControl_ddlPageSize")
drop_down_num_page.send_keys("500 per page")
symbol = driver.find_elements_by_xpath("//td[contains(@class, 'gridSymbol')]")
sector = driver.find_elements_by_xpath("//td[contains(@class, 'gridSectorName')]")
industry = driver.find_elements_by_xpath("//td[contains(@class, 'gridIndustryName')]")

symbol_list = [i.text for i in symbol]
sector_list = [i.text for i in sector]
industry_list = [i.text for i in industry]

next_button = driver.find_elements_by_xpath("//a[contains(@href, 'ContentPlaceHolder') and contains(@href, 'AspNetPager')]")[0]
next_button.click()

symbol2 = driver.find_elements_by_xpath("//td[contains(@class, 'gridSymbol')]")
sector2 = driver.find_elements_by_xpath("//td[contains(@class, 'gridSectorName')]")
industry2 = driver.find_elements_by_xpath("//td[contains(@class, 'gridIndustryName')]")

symbol_list = symbol_list + [i.text for i in symbol2]
sector_list = sector_list + [i.text for i in sector2]
industry_list = industry_list + [i.text for i in industry2]

stock_sector_df = pd.DataFrame(list(zip(symbol_list, sector_list, industry_list)), 
               columns =['symbol', 'sector','industry']) 

#stock_name = []
#pe_list = []
#stock_data_list = []
#column_max_len = []
#max_len_column_names = 0
stock_df = pd.DataFrame()


for i in range(stock_sector_df.shape[0]):
    stock = str(stock_sector_df.iloc[i,0]).upper()
    ch_url = 'https://www.set.or.th/set/companyhighlight.do?symbol=' + urllib.parse.quote(stock) +'&language=en&country=US'
    try:
        company_highlights = pd.read_html(ch_url)[0]
    except ValueError:
        pass
    if company_highlights.shape[0]>1 & (company_highlights.empty == False):
        #stock_name.append(stock)
        
        column_names = [elem1 for elem1, elem2 in company_highlights.columns] if type(company_highlights.columns[1]) is tuple else [elem for elem in company_highlights.columns]
        #max_len_column_names = len(column_names) if len(column_names) > max_len_column_names else max_len_column_names
        #column_max_len = column_names if len(column_names) >= max_len_column_names else column_max_len
        column_names[len(column_names)-1] = 'Current' if column_names[len(column_names)-1]=='Unnamed: 5' else column_names[len(column_names)-1]
        company_highlights.columns = column_names
        company_highlights = company_highlights.loc[(company_highlights[column_names[0]]!='Financial Data') & (company_highlights[column_names[0]]!='Financial Ratio')]
        company_highlights['Symbol'] = stock
        #stock_data_list.append(company_highlights)
        #print(company_highlights)
        #print(stock_df.empty)
        if stock_df.empty == True:
            stock_df = pd.melt(company_highlights, id_vars=[column_names[0],'Symbol'])
            #print(stock_df)
        else:
            stock_df = stock_df.append(pd.melt(company_highlights, id_vars=[column_names[0],'Symbol']))
        #pd.melt(company_highlights, id_vars=['Statistics as of','Symbol'])
        print(stock +' '+ str(round( ((i+1)/(stock_sector_df.shape[0]))*100, 2)) +'%' + "  " + str(i) + "/" + str(stock_sector_df.shape[0]) )


