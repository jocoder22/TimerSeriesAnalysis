#!/usr/bin/env python
import os
import shutil
from pathlib import Path
from printdescribe import print2


################################ making and using temporary directories and files ###########################
####################################### use tempfile module #################################################
# 4 classes
## TemporaryFile, NamedTemporaryFile, TemporaryDirectory, and SpooledTemporaryFile
## mode are 'w+b' (default) for binary read and write, 'w+t' for text read and write
from tempfile import TemporaryFile, NamedTemporaryFile, TemporaryDirectory, SpooledTemporaryFile, gettempdir

# Create a temporary file and write some data to it
tf001 = TemporaryFile('w+t')
tf001.write('Hello Machine Learners!')

# Go back to the beginning and read data from file, cos the cursor is at the end after writing to the file
tf001.seek(0)
mydata = tf001.read()

# Close the file, after which it will be removed
tf001.close()

### can use context manager for authomatic closing
with TemporaryFile('w+t') as tf001:
  tf001.write('Hello Machine Learners!') # tf001.write(b'Hello Machine Learners!') for binary
  tf001.seek(0)
  tf001.read()
  # print(tempfile.gettempdir())
  print(gettempdir()) # print the tempfile directory in your system
  
  
  
########################################## create temporary directory #############################################
with TemporaryDirectory() as tempdir:
  print2(f'Created directory {tempdir}')
  os.path.exists(tempdir)
  os.path.is_dir(tempdir)
  os.path.dirname(tempdir)
  os.path.abspath(tempdir)
  
  
  
  ########################################### coping file and directory #############################################
  ########## copy single file #######################################################################################
  ######## shutil.copy2() will copy metadata, permission, attributes etc while .copy() will not ####################
  src_file = "\machineLearning\Adaboast.py"
  dst_dir = "\Adaboast\"
  shutil.copy(src_file, dst_dir)

  
  ####### using copytree(), will copy the entire directory trees and files within it #################################
  ########## create new folder, if not existing ######################################################################
  ########### Good for backing up your folders and files 
  shutil.copytree("Adaboast", "Adaboast_backup")
