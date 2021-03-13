#!/usr/bin/env python
import os
import shutil
from pathlib import Path

src = r"E:\Intradays"
dst = r"C:\Users\HP\Documents\Intradays"


folders = ['Apple', 'MicroSoft', 'Google', 'Netflix', 'Tesla', 'Amazon', 'Toyota', 'JPMorgan', 
            'Citigroup', 'Walmat', 'Target', "Fedex", "Ups", "Walgreens", "Disney", "Pfizer",
            "Cvs", "AT_T", "CocaCola", "Boeing", "SolarEdge", "AdvancedMicroDevices", "Twilio",
            "ExpWorld", "HomeDepot", "Ford", "PVH", "Twitter", "Salesforce", 
            "Alibaba", "NioElectricMotor", "Apple" ,  "BristolMyers"]
symbols = ['AAPL', 'MSFT', 'GOOGL', 'NFLX', 'TSLA', 'AMZN', 'TM', 'JPM', 'C', 'WMT', 'TGT', 'FDX',
            'UPS', 'WBA', 'DIS', 'PFE', 'CVS', 'T', 'KO', 'BA', 'SEDG', 'AMD', 'TWLO', 'EXPI', 'HD',
              'F', 'PVH', 'TWTR', 'CRM', 'BABA', 'NIO', 'AAPL', 'BMY']

def backUp(src, dst, symbols=symbols, folders=folders)
    for idx in range(len(symbols)):
        _src = os.path.join(src, folders[idx])
        _dst = os.path.join(dst, folders[idx])

        if not os.path.isdir(_dst):
            os.makedirs(_dst)
        
        for entry in os.listdir(_src):
            if entry in os.listdir(_dst): 
                continue
            else:
                myfile = os.path.join(_src, entry)
                shutil.copy(f"{myfile}", f"{_dst}")
                print()
                print(f"Copied {entry} to {_dst}")
