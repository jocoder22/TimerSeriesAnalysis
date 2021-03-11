#!/usr/bin/env python
import os
import shutil
import zipfile

############### reading zipfile, using context manager ################################
with zipfile.Zipfile("machineLearning.zip", "r") as zp:
  zp.namelist() # return a list of names of files in the zip file

  
###### get detailed on files in zip archive ############################################

def print_info()

with zipfile.Zipfile("machineLearning.zip", "r") as zp:
  for path_name in zp.namelist():
    if path_name.is_dir():
      
     else:
        file_info = zp.getinfo(path_name)
        print(f'File name: {file_info.filename}, File Size: {file_info.file_size}, 
              Compression Size: {file_info.compress_size}, Last Modified Date: {file_info.date_time}")
