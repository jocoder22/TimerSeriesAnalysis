#!/usr/bin/env python
import os
from pathlib import Path
from glob import glob
from fnmatch import fnmatch
# 3cfd9bbf-8676-4c82-b44b-93fc69bd4ede

  
################################# creating directory #####################################################
# if directory or path already exists, mkdir() raises a FileExistsError:
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



############################### Making multiple directories ###############################################
### use os.mkdirs, ===> not the s (similar to mkdir without the s) ########################################
# The permission (owner and group users) default mode is 0o777
os.mkdirs("PythonLearning/machineLearning/AdaBoost/", mode = 0o777)
# os.mkdirs("PythonLearning3/machineLearning{1..2}"/)


p = Path("PythonLearning/machineLearning/AdaBoost/")
p.mkdir(parents=True)


#  os.makedirs() and Path.mkdir() raise an OSError if the target directory already exists.
# use exist_ok = true to avoid throwing eht OSError
# $ tree -p -i .

############# shell command
# $ mkdir PythonLearning
# $ cd PythonLearning/
# $ mkdir machineLearning
# $ touch machineLearning/file1.py machineLearning/file2.py machineLearning/mytext.txt
# $ touch data_{01..03}.cvs data_{01..03}_backup.cvs text_{01..03}.txt admin.py tests.py

# $ mkdir PythonLearning2
# $ cd PythonLearning2/
# $ mkdir machineLearning1 machineLearning1
# $ touch machineLearning1/file1.py machineLearning1/file2.py machineLearning1/file3.py
# $ touch machineLearning2/file4.py machineLearning2/file5.py machineLearning2/file6.py 
# $ touch data_{01..03}.cvs data_{01..03}_backup.cvs text_{01..03}.txt admin.py tests.py

