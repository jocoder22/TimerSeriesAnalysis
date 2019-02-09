#!/usr/bin/env python
from librosa.display import specshow
from librosa.core import amplitude_to_db
from librosa.core import stft
from sklearn.model_selection import cross_val_score
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

# # file1 = 'C:\\Users\\okigboo\Desktop\\TimeSeriesAnalysis\\machineLearning\\maky.wav'
# file1 = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\maky.wav'
# audio, sfreq = lr.load(file1)
# print(type(audio), type(sfreq))
# print(audio.shape)
# print(sfreq)

# # time = np.arange(audio.shape[0]) / sfreq
# time = np.arange(0, len(audio)) / sfreq
# print(len(time))

# print(audio)

# normal = pd.DataFrame({'time': time, 'audio': audio}).set_index('time')
# print(normal.head())
# print(normal.tail())

# normal.plot()
# plt.show()
# # Plot audio over time
# fig, ax = plt.subplots()
# ax.plot(time, audio)
# ax.set(xlabel='Time (s)', ylabel='Sound Amplitude')
# plt.show()


from pydub import AudioSegment
# path = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\machineLearning\\'
# path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\'
# os.chdir(path)

# src = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\maky2.mp3"
# dst = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\test1.wav"

src = "C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/maky2.mp3"
dst = "C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/test1.wav"

# song = AudioSegment.from_mp3("C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/maky2.mp3")
# song.export("C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/test1.wav", format="wav")







import pydub
sound = pydub.AudioSegment.from_mp3("C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\maky2.mp3")
# sound.export("D:/example/apple.wav", format="wav")








# import subprocess

# subprocess.call(['ffmpeg', '-i', src,
#                    dst])

# ticker = ['AAPl', 'FB', 'NFLX', 'V', 'XOM']
# data = pdr.get_data_yahoo(ticker, starttime, endtime)['Adj Close']

# print(data.head())

# # Loop through each column, plot its values over time
# fig, ax = plt.subplots()
# for column in data.columns:
#     data[column].plot(ax=ax, label=column)
# ax.legend()
# plt.show()


# # Rectify the audio signal
audio = pd.Series(audio)
audio_rectified = audio.apply(np.abs)

# Plot the result
audio_rectified.plot()
plt.show()


# Smooth by applying a rolling mean
# roll = int(np.sqrt(audio.shape[0]))
roll = int(audio.shape[0] / sfreq  * 90)
audio_rectified_smooth = audio_rectified.rolling(roll).mean()

# Plot the result
audio_rectified_smooth.plot()
plt.show()


# # Calculate stats
# means = np.mean(audio_rectified_smooth, axis=0)
# stds = np.std(audio_rectified_smooth, axis=0)
# maxs = np.max(audio_rectified_smooth, axis=0)

# # Create the X and y arrays
# label = 'nomal'
# labels = np.array(label)
# X = np.column_stack([means, stds, maxs])
# y = labels.reshape([-1, 1])

# Fit the model and score on testing data
# percent_score = cross_val_score(model, X, y, cv=5)
# print(np.mean(percent_score))

# print(X, y)
# tempos = []
# for col, i_audio in audio.items():
#     tempos.append(lr.beat.tempo(i_audio.values, sr=sfreq,
#                                 hop_length=2**6, aggregate=None))

# # Convert the list to an array so you can manipulate it more easily
# tempos = np.array(tempos)

# # Calculate statistics of each tempo
# tempos_mean = tempos.mean(axis=-1)
# tempos_std = tempos.std(axis=-1)
# tempos_max = tempos.max(axis=-1)

audio = audio.values
print(audio[:10])
# tempos = lr.beat.tempo(audio, sr=sfreq,
#                         hop_length=2**6, aggregate=None)


# Prepare the STFT
HOP_LENGTH = 2**4
spec = stft(audio, hop_length=HOP_LENGTH, n_fft=2**7)

print(type(spec))
print(spec)
print(spec.shape)
# Convert into decibels
spec_db = amplitude_to_db(np.abs(spec))

# # Compare the raw audio to the spectrogram of the audio
# fig, axs = plt.subplots(2, 1, figsize=(10, 10), sharex=True)
# axs[0].plot(time, audio)
# specshow(spec_db, sr=sfreq, x_axis='time', y_axis='hz', hop_length=HOP_LENGTH)
# plt.show()


# Calculate the spectral centroid and bandwidth for the spectrogram
# bandwidths = lr.feature.spectral_bandwidth(S=spec)[0]
# centroids = lr.feature.spectral_centroid(S=spec)[0]

bandwidths = lr.feature.spectral_bandwidth(S=spec)[0]
centroids = lr.feature.spectral_centroid(S=spec)[0]


# Convert spectrogram to decibels for visualization
spec_db = amplitude_to_db(spec)

# Display these features on top of the spectrogram
fig, ax = plt.subplots(figsize=(10, 5))
ax = specshow(spec_db, x_axis='time', y_axis='hz', hop_length=HOP_LENGTH)
ax.plot(times_spec, centroids)
ax.fill_between(times_spec, centroids - bandwidths / 2,
                centroids + bandwidths / 2, alpha=.5)
ax.set(ylim=[None, 6000])
plt.show()

