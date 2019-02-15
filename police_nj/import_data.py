from zipfile import ZipFile
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import pandas as pd
import os
import gzip
import io
import csv


path = 'C:\\Users\\okigboo\\Desktop\\TimeSeriesAnalysis\\police_nj\\'
os.chdir(path)


# Create file path: file_path
url = 'https://stacks.stanford.edu/file/druid:py883nd2578/NJ-clean.csv.gz'


# zipper = ZipFile("NJ-clean.csv.gz")
# data = pd.read_csv(zipper.open('NJ_cleaned.csv'), sep=',', engine="python")
# filename = url.split('/')[-1]
# with open(filename, "wb") as f:
#     r = requests.get(url)
#     f.write(r.content)


# # with gzip.open(filename, mode="rt") as f:
# with gzip.open("NJ-clean.csv.gz", "rt", newline="") as file:
#     reader = csv.reader(file)
#     print(list(reader))

# df = pd.read_csv('NJ_cleaned.csv')
# print(df.columns)


url2 = 'https://assets.datacamp.com/production/repositories/1497/datasets/62bd9feef451860db02d26553613a299721882e8/police.csv'
RI =  pd.read_csv(url2, sep=',')
print(RI.shape)
print(RI.columns)


url3 = 'https://assets.datacamp.com/production/repositories/1497/datasets/02f3fb2d4416d3f6626e1117688e0386784e8e55/weather.csv'
w = pd.read_csv(url3, sep=',')
print(w.shape)
print(w.columns)

print(RI.info())
print(RI.shape)
print(RI.isnull().sum()) # counts the number of missing values in each columns