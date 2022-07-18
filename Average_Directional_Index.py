# https://lessonsfinancial.com/2020/04/16/edu-campaign-six-indicators/?gclid=EAIaIQobChMIh9rX9O708AIVhdzICh0ZyAAXEAAYASAAEgIM8fD_BwE
#!/usr/bin/env python
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf
from ta.trend import ADXIndicator

aapl = yf.download('AAPL', '2017-1-1','2021-2-18')

aapl['Adj Open'] = aapl.Open * aapl['Adj Close']/aapl['Close']
aapl['Adj High'] = aapl.High * aapl['Adj Close']/aapl['Close']
aapl['Adj Low'] = aapl.Low * aapl['Adj Close']/aapl['Close']
aapl.dropna(inplace=True)


adxI = ADXIndicator(aapl['Adj High'],aapl['Adj Low'],aapl['Adj Close'], 20,False)
aapl['pos_directional_indicator'] = adxI.adx_pos()
aapl['neg_directional_indicator'] = adxI.adx_neg()
aapl['adx'] = adxI.adx()

print(aapl.tail())


def plot_graph(data,ylabel,xlabel):
    plt.figure(figsize=(10,7))
    plt.grid()
    plt.plot(data)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

    
plot_graph(aapl['Adj Close'], 'Price', 'Date')
plot_graph(aapl['adx'], 'Price', 'Date')

plt.plot(aapl['Adj Close'], label='Adj Close')
plt.plot(aapl['adx'], label='adx')
plt.grid()
plt.legend(loc='upper right')
# plt.show()


aapl['trend'] = np.where(aapl.adx>25,aapl['Adj Close'],np.nan)

aapl['trend_signal'] = np.where(aapl.adx>25,1,0)
plt.figure(figsize=(10,7))
plt.grid()
plt.plot(aapl['Adj Close'],  label='Adj Close')
plt.plot(aapl['trend'], label='trend')
plt.ylabel('Price')
plt.xlabel('Date')
plt.legend(loc='upper left')
plt.show()


aapl['direction'] = np.where(aapl.pos_directional_indicator>aapl.neg_directional_indicator,1,-1) * aapl['trend_signal']
aapl['daily_returns'] = aapl['Adj Close'].pct_change()
aapl['strategy_returns'] = aapl.daily_returns.shift(-1) * aapl.direction
plot_graph((aapl['strategy_returns']+1).cumprod(), 'Returns', 'Date')
plt.show()




