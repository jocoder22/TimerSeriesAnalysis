#!/usr/bin/env python
import os
import shutil
from pathlib import Path
from printdescribe import  changepath

src = r"C:\Users\HP\Documents\capstone"
# src = r"C:\Users\HP\Documents\capstone"
# dst = r"D:\Capstone"
dst = r"E:\Capstone"


def copy_all_files(_dstt, src=src):
    """Print name of all files in given path and subdirs."""

    for entry in os.scandir(src):
        if entry.is_dir(follow_symlinks=False):
            _src = os.path.join(src, entry)
            print(_src)

            
            _dst = os.path.join(_dstt, entry.name)
            print(_dst)
            print("\n\n")

            if not os.path.isdir(_dst):
                os.makedirs(_dst)

            for entry2 in os.listdir(_src):
                if entry2 in os.listdir(_dst): 
                    continue

        else:
            myfile = os.path.join(_src, entry)
            shutil.copy(f"{myfile}", f"{_dst}")
            print(f"Copied {entry} to {_dst}")

            if entry2 == os.listdir(_src)[-1]:
                print()


# copy_all_files(dst)


def copy_all_files2(_dstt, src=src):
    """Print name of all files in given path and subdirs."""

    for entry in os.scandir(src):
        if entry.is_dir(follow_symlinks=False):

            _src = os.path.join(entry)
            _dst = os.path.join(_dstt,  entry.name)

            if not os.path.isdir(_dst):
                os.makedirs(_dst)

            copy_all_files2(_dst, _src)

        else:
            myfile = os.path.join(src, entry)
            shutil.copy(f"{myfile}", f"{_dstt}")
            print(f"Copied {entry} to {_dstt}")
    
            if entry == os.listdir(src)[-1]:
                print()


copy_all_files2(dst)




# def print_all_files(path):
#     """Print name of all files in given path and subdirs."""
#     for entry in os.scandir(path):
#         if entry.is_dir(follow_symlinks=False):
#             print_all_files(entry.path)
#         else:
#           print(entry.name)