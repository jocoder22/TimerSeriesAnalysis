#!/usr/bin/env python
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as pdr
from datetime import datetime

# starttime = datetime(2010, 1, 1)
# endtime = datetime(2013, 12, 31)
# ticker = 'AAPL'
# data = pdr.get_data_yahoo(ticker, starttime, endtime)

# print(data.head(12))
# data['Close'].plot(title = "Apple stock daily closing price")
# plt.show()


# # Plot the time series in each dataset
# fig, axs = plt.subplots(2, 1, figsize=(5, 10), sharex=True)
# data.iloc[:1000].plot(y='Open', ax=axs[0])
# data.iloc[:1000].plot(y='Close', ax=axs[1])
# plt.tight_layout()
# plt.show()


# """ 
# # ploting time series 
# # using matplotlib
# fig, ax = plt.subplots()
# ax.plot(...)

# # using pandas
# fig, ax = plt.subplots()
# df.plot(ax=ax)

# """

# fig, ax = plt.subplots()
# plt.style.use('ggplot')
# apple2012close = data.loc['2012',['Close']]
# print(apple2012close.head())
# ax.plot(apple2012close, label='Weekly Close average')
# monthly = apple2012close.resample('W').mean()
# monthly.add_suffix('_monthly').plot(ax=ax)
# plt.legend()
# plt.show()


# # Audio data using librosa
import librosa as lr

file1 = 'C:\\Users\\okigboo\Desktop\\TimeSeriesAnalysis\\machineLearning\\maky.wav'
audio, sfreq = lr.load(file1)
print(type(audio), type(sfreq))
print(audio.shape)
print(sfreq)

# time = np.arange(audio.shape[0]) / sfreq
time = np.arange(0, len(audio)) / sfreq
print(len(time))

print(audio)

normal = pd.DataFrame({'time': time, 'audio': audio}).set_index('time')
print(normal.head())
print(normal.tail())

normal.plot()
plt.show()
# # Plot audio over time
# fig, ax = plt.subplots()
# ax.plot(time, audio)
# ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
# plt.show()


# from pydub import AudioSegment
# path = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\machineLearning\\'
# os.chdir(path)

# # src = "maky.mp3"
# # src2 = "C:/Users/okigboo/Desktop/TimeSeriesAnalysis/machineLearning/maky.mp3"
# # src2 = 'C:\\Users\\okigboo\Desktop\\TimeSeriesAnalysis\\machineLearning\\maky2.mp3'

# # # dst = "test1.wav"
# # # song = AudioSegment.from_mp3(src2)
# # # song.export(dst, format="wav")


# # import subprocess

# # subprocess.call(['ffmpeg', '-i', src2,
# #                    dst])

# ticker = ['AAPl', 'FB', 'NFLX', 'V', 'XOM']
# data = pdr.get_data_yahoo(ticker, starttime, endtime)['Adj Close']

# print(data.head())

# # Loop through each column, plot its values over time
# fig, ax = plt.subplots()
# for column in data.columns:
#     data[column].plot(ax=ax, label=column)
# ax.legend()
# plt.show()


# Rectify the audio signal
audio = pd.Series(audio)
audio_rectified = audio.apply(np.abs)

# Plot the result
audio_rectified.plot()
plt.show()
