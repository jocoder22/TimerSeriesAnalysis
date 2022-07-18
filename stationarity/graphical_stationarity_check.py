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


aapl = yf.download('AAPL', '2017-1-1','2021-2-18')

plot_graph(aapl['Adj Close'], 'Price', 'Date')