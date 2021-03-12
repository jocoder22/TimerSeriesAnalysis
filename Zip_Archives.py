#!/usr/bin/env python
import os
import shutil
import zipfile
from pathlib import Path

############### reading zipfile, using context manager ################################
with zipfile.Zipfile("machineLearning.zip", "r") as zp:
  zp.namelist() # return a list of names of files in the zip file

  
###### get detailed on files in zip archive ############################################

def print_info(path_name2):
  file_info = zp.getinfo(path_name2)
  print(f'File name: {file_info.filename}, File Size: {file_info.file_size}, 
        Compression Size: {file_info.compress_size}, Last Modified Date: {file_info.date_time}")


with zipfile.Zipfile("machineLearning.zip", "r") as zp:
  for path_name in zp.namelist():
    if path_name.is_dir():
#         continue
        for entry in os.scandir(path_name):
          print_info(entry)
        
     else:
        print_info(path_name)

              
def print_all_files(path):
    """Print name of all files in given path and subdirs."""
    for entry in os.scandir(path):
        if entry.is_dir(follow_symlinks=False):
            print_all_files(entry.path)
        else:
          print(entry.name)
 
  
        
########################### extract Zip file ##########################################################
######### extract one file
with zipfile.Zipfile("machineLearning.zip", "r") as zp:
        zp.extract("pythonLearn.py") # to current working directory
        zp.extract("pythonLearn.py", path="machineLearning2/") # to another directory
        

############ extract all files 
with zipfile.Zipfile("machineLearning.zip", "r") as zp:
        zp.extractall() # to current working directory
        zp.extractall(path="machineLearning2/") # to another directory
        zp.extractall(path="machineLearning2/", pwd='password') # to another directory, with password protected zip
  
        
################################## creating zip file ####################################################
with os.scandir('newMachineLearning/') as entries:
        with zipfile.ZipFile('newMachineLearning.zip', 'w') as zp:
          for file in entries:
              zp.write(file)
        

        
# # using pathlib Path
# with zipfile.ZipFile('newMachineLearning.zip', 'w') as zp:
#     for entry in Path('newMachineLearning/').iterdir():
#        zp.write(entry.name)        
 
        
# # using pathlib Path
# entries = Path('newMachineLearning/')
# with zipfile.ZipFile('newMachineLearning.zip', 'w') as zp:
#     for entry in entries.iterdir():
#        zp.write(entry.name)
#             
