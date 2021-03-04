#!/usr/bin/env python
import os
from pathlib import Path


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



# os.listdir() is old, don't use it
entries = os.listdir('my_directory/')
for entry in entries:
  print(entry)
  

# os.scandir() and pathlib modules are newer! use them
# os.scandir() returns an posix.ScandirIterator object, which is an iterator
with os.scandir('my_directory/') as entries:
    for entry in entries:
        print(entry.name)  

        
# using pathlib Path
entries = Path('my_directory/')
for entry in entries.iterdir():
    print(entry.name)        
    
    
# $ tree -p -i   



#############################################  List all files in a directory  ############################
# List all files in a directory using os.listdir
basepath = 'my_directory/'
for entry in os.listdir(basepath):
    if os.path.isfile(os.path.join(basepath, entry)):
        print(entry)
        
# List all files in a directory using scandir()
basepath = 'my_directory/'
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_file():
            print(entry.name)       

# List all files in a directory using pathlib Path            
basepath = Path('my_directory/')
files_in_basepath = basepath.iterdir()
for item in files_in_basepath:
    if item.is_file():
        print(item.name)
 
# for item in files_in_basepath:if item.is_file():
#         print(item.name)

# List all files in directory using pathlib, using generator expresssion
basepath = Path('my_directory/')
files_in_basepath = (entry for entry in basepath.iterdir() if entry.is_file())
for item in files_in_basepath:
    print(item.name)
    

#####################################  List all subdirectories ####################################
# List all subdirectories using os.listdir
basepath = 'my_directory/'
for entry in os.listdir(basepath):
    if os.path.isdir(os.path.join(basepath, entry)):
        print(entry)    
    
# List all subdirectories using scandir()
basepath = 'my_directory/'
with os.scandir(basepath) as entries:
    for entry in entries:
        if entry.is_dir():
            print(entry.name)
            
            
 # List all subdirectory using pathlib
basepath = Path('my_directory/')
for entry in basepath.iterdir():
    if entry.is_dir():
        print(entry.name)
        
        
############################################# print file name in director and subdirectories ############        
def print_all_files(path):
    """Print name of all files in given path and subdirs."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            print_all_files(entry.path)
        else:
          print(entry.name)
 
  
 def get_tree_size(path):
    """Return total size of files in given path and subdirs."""
    total = 0
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            total += get_tree_size(entry.path)
        else:
            total += entry.stat(follow_symlinks=False).st_size
    return total
  
  
################################# creating directory #####################################################
# if directory or path already exists, mkdir() raises a FileExistsError:
import os
from pathlib import Path

# using os module
os.mkdir('example_directory/')

# pathlib module
p = Path('example_directory/')
p.mkdir()

# can use try-except to catch the error
try:
    p.mkdir()
except FileExistsError as e:
    print(e)

# can ignore the FileExistsError by passing the exist_ok=True 
p.mkdir(exist_ok=True)


