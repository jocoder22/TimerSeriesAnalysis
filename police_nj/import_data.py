from zipfile import ZipFile
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import pandas as pd


# Create file path: file_path


url = 'https://stacks.stanford.edu/file/druid:py883nd2578/NJ-clean.csv.gz'
response = requests.get(url)

data = pd.read_csv(response)

print(data.head())


# with open(filename, "wb") as f:
#     r = requests.get(url)
#     f.write(r.content)


# mylist = [filename for filename in zipp.namelist()]

