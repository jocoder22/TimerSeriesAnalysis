#!/usr/bin/env python
import os
from pathlib import Path
from glob import glob
from fnmatch import fnmatch
from datetime import datetime, timedelta, date

from printdescribe import print2, changepath

path1 = r"E:\Intradays\AdvancedMicroDevices"

with os.scandir(path1) as entries:
    for entry in entries:
        print(entry.name)  


def convert_date(timestamp):
    d = datetime.utcfromtimestamp(timestamp)
    formated_date = d.strftime("%d_%b_%Y")
    # datt2 = dattt.strftime("%d_%b_%Y")
    return formated_date

def get_files():
    dir_entries = os.scandir(path1)
    for entry in dir_entries:
        if entry.is_file():
            info = entry.stat()
            print(f'{entry.name}\t Last Modified: {convert_date(info.st_mtime)}')

get_files()

limitday = 40
stdate = date.today() - timedelta(days=limitday)
print2(stdate)