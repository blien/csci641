'''
Created on Dec 2, 2018

@author: brandon
'''

import sys
import scipy as sp
import numpy as np
import matplotlib as plt
import json
import glob, os
from pprint import pprint
import fnmatch


def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)

def findDataFiles():
    for root, dirs, files in os.walk('E:\\School\\CSCI-641\\tarfiles\\keys'):
        for file in files:
            if file.endswith(".txt"):
                 print(os.path.join(root, file))
    
    """
    for file in os.listdir('E:\\School\\CSCI-641\\tarfiles\\keys'):
        if file.endswith(".txt"):
            print(os.path.join('E:\\School\\CSCI-641\\tarfiles\\keys', file))
    """

def readAndPrintFile():
    with open('E:\\School\\CSCI-641\\tarfiles\\keys\\17\\1700000.txt', 'r') as f:
        f.readline()
        for line in f:
            print(line)


def readJsonFiles ():
    print("reading E:\\School\\CSCI-641\\tarfiles\\keys\\17\\1700000.tx:")
    json_data = []
    with open("E:\\School\\CSCI-641\\tarfiles\\keys\\18\\1800011.txt") as json_file:
        for line in json_file:
            #print(line)
            cur_jason = json.loads(line)
            #print (json.dumps(cur_jason, indent = 4, sort_keys=True))
            """
            for key, value in cur_jason.items():
                pprint(key)
            """
            keys = []
            get_keys(cur_jason, keys)
            
            print(keys)
            json_data.append(cur_jason)

            #json_data.append(json.load(line))
    print("Finished reading file")

    #print(json.dumps(json_data))
    #print(json_data)

def main():
    print("Hello world!")
    findDataFiles()
    # readJsonFiles()
    # readAndPrintFile()
    print("End of file")

if __name__ == '__main__':
    main()