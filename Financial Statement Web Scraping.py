# -*- coding: utf-8 -*-
"""
Created on Sun Dec 29 13:46:19 2019

@author: YIT
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 15:34:58 2019

@author: Santi
"""


import pandas as pd
#import pickle

#### load data ####
dir_name = "C:\\Users\\YIT\\Python Stock Analysis\\"
stock_sector= pd.read_excel(dir_name + 'Stock Sector.xlsx')
stock_sector = stock_sector.loc[stock_sector['Symbol'].notnull(), :]
# remove REIT companies
stock_sector = stock_sector.loc[stock_sector['Industry Name'].str.startswith('REIT') == False, :]

## delete stocks that contain '-'
#stock_sector = stock_sector[stock_sector['Symbol'].str.contains('-') == False]

colname = stock_sector.columns
stock_sector.columns = [ 'Dividend Yield(%)' if x== 'Dividend Yield' else x  for x in colname]

stock_sector['Market Cap (m)'] = pd.to_numeric(stock_sector['Market Cap (m)'], errors='coerce')

sector = stock_sector.groupby('Stock Sector').agg({'Market Cap (m)':'sum'})
industry = stock_sector.groupby('Industry Name').agg({'Market Cap (m)':'count'})


stock_name = []
pe_list = []
stock_data_list = []
column_max_len = []
max_len_column_names = 0
for i in range(stock_sector.shape[0]):
    stock = str(stock_sector.iloc[i,0]).upper()
    ch_url = 'https://www.set.or.th/set/companyhighlight.do?symbol=' + stock +'&language=en&country=US'
    try:
        company_highlights = pd.read_html(ch_url)[0]
    except ValueError:
        company_highlights = pd.DataFrame()
        pass
    if company_highlights.empty == False:
        stock_name.append(stock)
        column_names = [dat for  i, dat in company_highlights.columns]
        max_len_column_names = len(column_names) if len(column_names) > max_len_column_names else max_len_column_names
        column_max_len = column_names if len(column_names) >= max_len_column_names else column_max_len
        company_highlights.columns = column_names
        company_highlights = company_highlights.loc[(company_highlights['Statistics as of']!='Financial Data') & (company_highlights['Statistics as of']!='Financial Ratio')]
        company_highlights['Symbol'] = stock
        stock_data_list.append(company_highlights)
        print(stock +' '+ str(round( ((i+1)/(stock_sector.shape[0]))*100, 2)) +'%')



# append all the dataframes
finance_info = pd.concat(stock_data_list,sort=False)   
statistics_name = finance_info['Statistics as of'].unique()

# clean environment
if 'stock_data_list' in locals().keys():
    del stock_data_list
#########

finance_info2 = pd.merge(finance_info, stock_sector, on = 'Symbol', how='left')

#stock_sector.groupby('Symbol').agg({'Symbol':'count'})
finance_info2.to_csv(dir_name + 'finance info.csv')

finance_info2.loc[finance_info2['Statistics as of']=='P/E',:].groupby('Industry Name').agg({'21/12/2019':'sum'})
#### save to disk
'''
with open('C:\\Users\YIT\Python Stock Analysis\stock_data_list.pickle', 'wb') as f:
    pickle.dump(stock_data_list, f)
with open('C:\\Users\YIT\Python Stock Analysis\stock_name.pickle', 'wb') as f:
    pickle.dump(stock_name, f)


with open('C:\\Users\YIT\Python Stock Analysis\stock_data_list.pickle', 'rb') as f:
    stock_data_list = pickle.load(f)
with open('C:\\Users\YIT\Python Stock Analysis\stock_name.pickle', 'rb') as f:
    stock_name = pickle.load(f)
'''

#########

#pe_list.append(company_highlights.loc[company_highlights['Statistics as of']=='P/E',company_highlights.columns[-1]])

### prepare dataframe for retrieving financial info.


