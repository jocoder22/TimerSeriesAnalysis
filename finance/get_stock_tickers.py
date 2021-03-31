
import requests
import pandas as pd
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

        
    data = pd.DataFrame(columns = ['Company_Name',  'Company_Ticker']) 
    
    data['Company_Name'] = name
    data['Company_Ticker'] = ticker
    
    return data

mmm = string.ascii_uppercase + "0"
