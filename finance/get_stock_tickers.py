
import requests
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, date
from bs4 import BeautifulSoup
import string


def get_stock_tickers(alphabet):
    name =[]
    ticker = []
    
    for char in alphabet: 
        URL =  f'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={char}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        items = [i for s in ['tr.ts0', 'tr.ts1'] for i in soup.select(s)]
    
        for i in items:
            row = i.find_all('td')
            name.append(row[0].text.strip())
            ticker.append(row[1].text.strip())

        
    data = pd.DataFrame(columns = ['CompanyName',  'CompanyTicker']) 
    
    data['CompanyName'] = name
    data['CompanyTicker'] = ticker
    
    return data


def get_stock_tickers2(alphabet):
    
    name =[]
    ticker = []
    closePrice = []
    startdate = date.today()
    
    for char in alphabet: 
        URL =  f'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={char}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        items = [i for s in ['tr.ts0', 'tr.ts1'] for i in soup.select(s)]
    
        for i in items:
            row = i.find_all('td')
            name.append(row[0].text.strip())
            tt = row[1].text.strip()
            ticker.append(tt)
            
            try:
                closePrice.append(pdr.get_data_yahoo(tt, startdate)['Adj Close'].values[0])
            except:
                closePrice.append(0.00)

        
    data = pd.DataFrame(columns = ['CompanyName',  'CompanyTicker', 'AdjustedClosePrice'])
    
    
    data['CompanyName'] = name
    data['CompanyTicker'] = ticker
    data['AdjustedClosePrice'] = closePrice
    
    return data

mmm = string.ascii_uppercase + "0"

ddd = get_stock_tickers(mmm)
