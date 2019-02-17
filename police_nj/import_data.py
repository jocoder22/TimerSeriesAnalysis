from zipfile import ZipFile
from io import BytesIO
import matplotlib.pyplot as plt
import pandas as pd
import os
import gzip
import io
import csv
import requests
import shutil



# path = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\police_nj\\'
path = 'C:\\Users\\Jose\\Desktop\\TimerSeriesAnalysis\\police_nj\\'
os.chdir(path)


# Creating a gzip or gz files
with open('Data.csv', 'rb') as infile:
    with gzip.open('data.csv.gz', 'wb') as outfile:
        shutil.copyfileobj(infile, outfile)


# Reading gzip or gz files
with gzip.open('data.csv.gz', 'rb') as gzfile:
    df = pd.read_csv(gzfile)


with open(requests.get(url).content, 'rb') as mydata:
    df3 = pd.read_csv(mydata)

# Create file path: file_path
url = 'https://stacks.stanford.edu/file/druid:py883nd2578/NJ-clean.csv.gz'

""" 
filename = url.split('/')[-1]
with open(filename, "wb") as f:
    r = requests.get(url)
    f.write(r.content)


# # with gzip.open(filename, mode="rt") as f:
# with gzip.open("NJ-clean.csv.gz", "rt", newline="") as file:
#     reader = csv.reader(file)
#     print(list(reader))

df = pd.read_csv('NJ_cleaned.csv', nrows=5)

tts = []
for chunk in pd.read_csv('NJ_cleaned.csv', chunksize=100000):
    chunky = pd.DataFrame(chunk)
    tts.append(chunk)
df3 = pd.concat(tts)

del tts

print(df3.shape)
print(df3.columns)
"""

url2 = 'https://assets.datacamp.com/production/repositories/1497/datasets/62bd9feef451860db02d26553613a299721882e8/police.csv'
RI =  pd.read_csv(url2, sep=',')
RI.to_csv('Data.csv', index=False)
print(RI.shape)
print(RI.columns)

""" 
url3 = 'https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv'
w = pd.read_csv(url3, sep=',')
print(w.shape)
print(w.columns)

print(RI.info())
print(RI.shape)
print(RI.isnull().sum()) # counts the number of missing values in each columns


# Drop the 'county_name' and 'state' columns
RI.drop(['county_name', 'state'], axis='columns', inplace=True)


df5 = pd.DataFrame([[1, 2], [3, 4]], columns=list('AB'))
df6 = pd.DataFrame([[5, 6], [7, 8]], columns=list('AB'))
df5.append(df6)
"""