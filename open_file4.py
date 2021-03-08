#!/usr/bin/env python
import os
from pathlib import Path
from glob import glob
from fnmatch import fnmatch


################################ making and using temporary directories and files ###########################
####################################### use tempfile module #################################################
# 4 classes
## TemporaryFile, NamedTemporaryFile, TemporaryDirectory, and SpooledTemporaryFile
## mode ar 'w+b' for binary read and write, 'w+t' for text read and write
from tempfile import TemporaryFile, NamedTemporaryFile, TemporaryDirectory, and SpooledTemporaryFile

# Create a temporary file and write some data to it
tf001 = TemporaryFile('w+t')
tf001.write('Hello universe!')

# Go back to the beginning and read data from file, cos the cursor is at the end after writing to the file
tf001.seek(0)
mydata = tf001.read()

# Close the file, after which it will be removed
tf001.close()
