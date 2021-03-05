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


