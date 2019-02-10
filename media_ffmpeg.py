import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn import datasets
plt.style.use('ggplot')
import subprocess
import pydub

import os

path = 'C:\\Users\\Jose\Desktop\\TimerSeriesAnalysis\\machineLearning'

os.chdir(path)



def convert_video(video_input, video_output):
    cmds = ['ffmpeg', '-i', video_input, video_output]
    subprocess.Popen(cmds, shell=True)

convert_video('maky2.mp3', 'test.wav')

print(os.getcwd())

def extract_audio(video, audio):
    command = f"ffmpeg -i {video} -ac 1  -f wav -vn {audio}"
    subprocess.call(command,shell=True)

extract_audio('myvideo.mp4','audio-new.wav')








from pydub import AudioSegment
# path = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\machineLearning\\'
# path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\'
# os.chdir(path)

# src = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\maky2.mp3"
# dst = "C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\machineLearning\\test1.wav"

src = "C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/maky2.mp3"
dst = "C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/test1.wav"

song = AudioSegment.from_mp3("C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/maky2.mp3")
song.export("C:/Users/Jose/Desktop/TimerSeriesAnalysis/machineLearning/test1.wav", format="wav")
