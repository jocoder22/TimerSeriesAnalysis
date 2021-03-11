#!/usr/bin/env python
import os
import shutil
import zipfile

############### reading zipfile, using context manager ################################
with zipfile.Zipfile("machineLearning.zip", "r") as zp:
  zp.namelist() # return a list of names of files in the zip file
