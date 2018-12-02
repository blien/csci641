'''
Created on Dec 2, 2018

@author: brandon
'''

import sys
import scipy as sp
import numpy as np
import matplotlib as plt
import json


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
            print (json.dumps(cur_jason, indent = 4, sort_keys=True))
            json_data.append(cur_jason)

            #json_data.append(json.load(line))
    print("Finished reading file")

    #print(json.dumps(json_data))
    #print(json_data)

def main():
    print("Hello world!")
    readJsonFiles()
    # readAndPrintFile()

if __name__ == '__main__':
    main()