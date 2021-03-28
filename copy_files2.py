#!/usr/bin/env python
import os
import shutil
from pathlib import Path
from printdescribe import  changepath

src = r"C:\Users\HP\Documents\capstone"
# src = r"C:\Users\HP\Documents\capstone"
# dst = r"D:\Capstone"
dst = r"E:\Capstone"


def copy_all_files2(_dstt, src=src):
    """copy all files in given path and subdirs to another file."""

    for entry in os.scandir(src):
        if entry.is_dir(follow_symlinks=False):

            # define source and destination paths
            _src = os.path.join(entry)
            _dst = os.path.join(_dstt,  entry.name)

            # create directory if not existing
            if not os.path.isdir(_dst):
                os.makedirs(_dst)

            # repeating recursively
            copy_all_files2(_dst, _src)

        else:
            # set the file path
            myfile = os.path.join(src, entry)

            # copy source file to distination
            shutil.copy(f"{myfile}", f"{_dstt}")
            print(f"Copied {entry} to {_dstt}")

            if entry == os.listdir(src)[-1]:
                print("Done coping!")

copy_all_files2(dst)

