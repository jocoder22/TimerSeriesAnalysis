#!/usr/bin/env python
import requests
import pandas as pd
import pandas_datareader as pdr
from datetime import datetime, date
from bs4 import BeautifulSoup
import string
from printdescribe import changepath
import time

path1 = r"E:\Capstone"


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


def get_stock_tickers2(alphabet, startdate=date.today()):
    
    name, ticker, closePrice = [], [], []
    # startdate = date.today()
    alphabet = alphabet.upper()
    
    for char in alphabet: 
        URL =  f'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={char}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        items = [i for s in ['tr.ts0', 'tr.ts1'] for i in soup.select(s)]
    
        for i in items:
            row = i.find_all('td')
            name.append(row[0].text.strip())
            ticker.append(row[1].text.strip())


    closePrice.append(pdr.get_data_yahoo(ticker, startdate)['Adj Close'].values[0])
        
    data = pd.DataFrame(columns = ['CompanyName',  'CompanyTicker', 'AdjustedClosePrice'])
    
    
    data['CompanyName'] = name
    data['CompanyTicker'] = ticker
    data['AdjustedClosePrice'] = closePrice[0]
    
    return data

if __name__ == "__main__":
    mmm = string.ascii_uppercase + "0"

    ddd = get_stock_tickers(mmm)

    # df2 = ddd.sort_values(by='AdjustedClosePrice', ascending=True, na_position='last')
    # ddd.query('AdjustedClosePrice < 12.0').sort_values(by='AdjustedClosePrice', ascending=True, na_position='last')


    # gg = ddd[ddd["AdjustedClosePrice"].isnull()]

    with changepath(path1):
        ddd.to_csv("tickers.csv")

    tickers = data.CompanyTicker.tolist()
    companies = data.CompanyName.tolist()

    startp = 0
endt = 10
for i in range(len(tickers)):
    startp = endt
    endt += 10
    closePrice.append(pdr.get_data_yahoo(tickers[startp:endt], start_)['Adj Close'].values[0])
    ticker.append(tickers[startp:endt])
    name.append(companies[startp:endt])
    data33 = pd.DataFrame(columns = ['CompanyName',  'CompanyTicker', 'AdjustedClosePrice'])
data33['CompanyName'] = name
data33['CompanyTicker'] = ticker
data33['AdjustedClosePrice'] = closePrice

path1 = r"E:\Capstone"
with changepath(path1):
        data33.to_csv("tickersplus.csv")


data['Price'] = [float(str(x).strip()[1:]) for x in data['Last Sale']]
newdata = data.iloc[:, [0,1,11]].sort_values('Price').query('Price  > 200.0 and Price < 400.0')
# https://www.nasdaq.com/market-activity/stocks/screener
# https://old.nasdaq.com/screening/companies-by-name.aspx
# https://github.com/shilewenuw/get_all_tickers/blob/master/get_all_tickers/get_tickers.py
# https://www.nasdaq.com/market-activity/stocks/screener
pd.set_option('display.max_colwidth', None)


# add ?raw=true
url = "https://github.com/shilewenuw/get_all_tickers/blob/master/get_all_tickers/tickers.csv?raw=true"
url = "https://github.com/jocoder22/TimerSeriesAnalysis/blob/master/finance/allstocks.csv?raw=true"
df = pd.read_csv(url, index_col=0)
print(df.head(5))
