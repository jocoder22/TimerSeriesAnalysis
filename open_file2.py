#!/usr/bin/env python
import os
from pathlib import Path

  
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


p = Path("PythonLearning/machineLearning/AdaBoost/")
p.mkdir(parents=True)


############# shell command
# $ mkdir PythonLearning
# $ cd PythonLearning/
# $ mkdir machineLearning
# $ touch machineLearning/file1.py machineLearning/file2.py
# $ touch data_{01..03}.cvs data_{01..03}_backup.cvs admin.py tests.py


#  os.makedirs() and Path.mkdir() raise an OSError if the target directory already exists.
# use exist_ok = true to avoid throwing eht OSError
# $ tree -p -i .

