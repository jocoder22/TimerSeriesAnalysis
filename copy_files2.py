#!/usr/bin/env python
import os
import shutil
from pathlib import Path
from printdescribe import  changepath

# src = r"C:\Users\HP\Documents\capstone"
# # src = r"C:\Users\HP\Documents\capstone"
# # dst = r"D:\Capstone"
# dst = r"E:\Capstone"

src = r"E:\Nopeee"
dst = r"D:\Nopeee"


def copy_all_files(_dstt, srca=src):
    """copy all files in given path and subdirs to another file."""

    for entry in os.scandir(srca):
        if entry.is_dir():

            # define source and destination paths
            _src = os.path.join(srca, entry)
            _dst = os.path.join(_dstt,  entry.name)

            # create directory if not existing
            if not os.path.isdir(_dst):
                os.makedirs(_dst)

            # repeating recursively
            copy_all_files2(_dst, _src)

        else:
                if entry in os.listdir(_dstt): 
                    print(f"{entry} already in {_dstt}", end="\n\n")
                    continue
            
                else:
                    # set the file path
                    myfile = os.path.join(src, entry) 
                    print(f'{myfile} ::::: {_dstt}')
                    # copy source file to distination
                    # shutil.copyfile(f"{myfile}", f"{_dstt}")
                    # print(f"Copied {entry} to {_dstt}")

                    if entry == os.listdir(src)[-1]:
                        print("Done coping!")


# copy_all_files(dst)


def copy_all_files2(_dstt, srca=src):
    """copy all files in given path and subdirs to another file."""

    for entry in os.scandir(srca):
        if entry.is_file(follow_symlinks=False):

            if entry in os.listdir(_dstt): 
                    continue
            
            else:
                    # set the file path
                    myfile = os.path.join(entry)

                    # copy source file to distination
                    shutil.copy(myfile, _dstt)
                    # print(f"Copied {entry} to {_dstt}")


        else:
            # define source and destination paths
            _src = os.path.join(entry)
            _dst = os.path.join(_dstt,  entry.name)

            # create directory if not existing
            if not os.path.isdir(_dst):
                os.makedirs(_dst)

            # # repeating recursively
            copy_all_files2(_dst, _src)



copy_all_files2(dst)