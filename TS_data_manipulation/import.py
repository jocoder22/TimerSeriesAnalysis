#!/usr/bin/env python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import pandas_datareader as pdr

ticker = ['RIO', 'ILMN', 'CPRT', 'EL', 'AMZN', 'PAA', 'GS', 'AMGN', 'MA', 'TEF', 'AAPL', 'UPS']

starttime = datetime.datetime(2010, 1, 4)
endtime = datetime.datetime(2019, 1, 31)
stocks = pdr.get_data_yahoo(ticker, starttime, endtime)['Adj Close']
stocks.fillna(method='backfill', inplace=True)

# Calculate the returns  
price_return = stocks.iloc[-1].div(stocks.iloc[0]).sub(1).mul(100)

# Plot horizontal bar chart of sorted price_return   
price_return.sort_values().plot(kind='barh', title='Stock Price Returns')
plt.show()


from datetime import datetime
import pandas_datareader.data as wb

ticker2 = ['AMD','GOOG','NYT', 'FB', 'CNF', 'AMZN','BABA']

start = datetime(2000,1,1)
end = datetime(2018,12,31)

stock2 = wb.DataReader(ticker2, 'yahoo',start,end)
print(type(stock2))
print(stock2.axes)
print(stock2.keys())
print(stock2['Adj Close'])
