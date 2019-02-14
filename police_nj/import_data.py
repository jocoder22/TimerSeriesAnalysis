from zipfile import ZipFile
from io import BytesIO
import requests
import matplotlib.pyplot as plt
import pandas as pd


# Create file path: file_path

url = 'https://stacks.stanford.edu/file/druid:py883nd25/NJ-clean.csv.gz'

response = requests.get(url)

# unzip the content

zipp = ZipFile(BytesIO(response.content))
print(zipp.namelist())

# mylist = [filename for filename in zipp.namelist()]
# mymedal2 = pd.read_csv(zipp.open(mylist[8]), sep='\t')
# # mymedal2 = pd.read_csv(zipp.open(file_path), sep='\t')

# # Load DataFrame from file_path: editions
# editions = pd.read_csv(zipp.open(mylist[8]), sep='\t')
# # editions = pd.read_csv(zipp.open(file_path), sep='\t')

# ioc_codes = pd.read_csv(zipp.open(mylist[9]))
# allmedals = pd.read_csv(zipp.open(mylist[7]), sep='\t', skiprows=4)
