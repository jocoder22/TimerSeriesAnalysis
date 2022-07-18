# https://www.analyticsvidhya.com/blog/2018/09/non-stationary-time-series-python/
#!/usr/bin/env python
import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt
import yfinance as yf

def plot_graph(data,ylabel,xlabel):
    """
    
    
    """
    plt.figure(figsize=(10,7))
    plt.grid()
    plt.plot(data)
    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.show()

sp = {"sep":"\n\n", "end":"\n\n"}
airpassengers = "E:\TimerSeriesAnalysis\datasets\AirPassengers.csv"

aapl = yf.download('AAPL', '2017-1-1','2022-6-30')
print(aapl.head(), **sp)

plot_graph(aapl['Adj Close'], 'Price', 'Date')


#reading the dataset
train = pd.read_csv(airpassengers)
print(train.head(), **sp)

#preprocessing
train["timestamp"] = pd.to_datetime(train.Month , format = '%Y-%m')
train.index = train.timestamp
train.drop('Month',axis = 1, inplace = True)

# train['#Passengers'].plot()
# plt.show()

plot_graph(train['#Passengers'], 'Number of Passengers', 'Date')

# there are trends (varing mean) in the above data 


# compute, monthly mean and variance and plot them
# both plots shows trending
aapl2 = aapl.reset_index()
month_mean = aapl2.resample('M', on="Date").mean()
month_var = aapl2.resample('M', on="Date").var()
plot_graph(month_mean['Adj Close'], 'Price', 'Date')
plot_graph(month_var['Adj Close'], 'Price', 'Date')


# compute moving 14 days moving averages and variance and plot them
df = aapl['Adj Close']
plt.plot(df,label=  'Adj Close')
plt.plot(df.rolling(9).mean(),label= 'MA 9 days')
plt.plot(df.rolling(21).mean(),label= 'MA 21 days')
plt.plot(df.rolling(9).var(),label= 'Mv 9 days')
plt.plot(df.rolling(21).var(),label= 'Mv 21 days')
plt.legend(loc='best')
plt.grid()
plt.title('Apple Adjusted Close \nMoving Averages and Moving Variances')
plt.show()