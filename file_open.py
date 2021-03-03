#!/usr/bin/env python

import os


with open('C:/captons/', 'rw') as f:
  data = f.read()
  # data = f.read(-5)
  # data2 = f.readline()
 

with open('filename.txt', 'r') as f:
    last_line = f.readlines()[-1]
    
    
from subprocess import Popen, PIPE
f = 'yourfilename.txt'
# Get the last line from the file
p = Popen(['tail','-1',f],shell=False, stderr=PIPE, stdout=PIPE)
res,err = p.communicate()
if err:
    print (err.decode())
else:
    # Use split to get the part of the line that you require
    res = res.decode().split('location="')[1].strip().split('"')[0]
    print (res)
 

import os
os.popen('tail -n 1000 filepath').read()


    
 with open('filename.txt', 'rb') as f:
    f.seek(-2, os.SEEK_END)
    while f.read(1) != b'\n':
        f.seek(-2, os.SEEK_CUR)
    last_line = f.readline().decode()
   
  
 with open('filename.txt') as f:
    for line in f:
        pass
    last_line = line
 

import csv

lis = list(csv.reader(open(inputFile)))
print lis[-1] # prints final line as a list of strings




entries = os.listdir('my_directory/')
for entry in entries:
  print(entry)
