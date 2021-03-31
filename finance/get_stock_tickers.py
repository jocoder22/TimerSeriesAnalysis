
import requests
import pandas as pd
from bs4 import BeautifulSoup
import string


def scrape_stock_symbols22(alphabet):
    company_name2 =[]
    company_ticker2 = []
    
    for char in alphabet: 
        URL =  f'https://www.advfn.com/nyse/newyorkstockexchange.asp?companies={char}'
        page = requests.get(URL)
        soup = BeautifulSoup(page.text, "html.parser")
        odd_rows = soup.find_all('tr', attrs= {'class':'ts0'})
        even_rows = soup.find_all('tr', attrs= {'class':'ts1'})

        for i in odd_rows:
            row = i.find_all('td')
            company_name2.append(row[0].text.strip())
            company_ticker2.append(row[1].text.strip())

        for i in even_rows:
            row = i.find_all('td')
            company_name2.append(row[0].text.strip())
            company_ticker2.append(row[1].text.strip())

        
    data = pd.DataFrame(columns = ['Company_Name',  'Company_Ticker']) 
    
    data['Company_Name'] = company_name2
    data['Company_Ticker'] = company_ticker2
    
    return data

mmm = string.ascii_uppercase + "0"
