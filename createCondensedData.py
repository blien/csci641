'''
Created on Dec 8, 2018

@author: brandon
'''

import sys
import scipy as sp
import numpy as np
import pandas as pd
#import matplotlib as plt
import json
import glob, os
from pprint import pprint
import fnmatch
import types

# function to get all json keys of json object
def getKeys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: getKeys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: getKeys(x, keys_list), dl)

def findDataFiles(startingDir):
    print(startingDir)
    jsonFiles = []
    for root, dirs, files in os.walk(startingDir):
        for file in files:
            if file.endswith(".txt"):
                jsonFiles.append(os.path.join(root, file))
                #print(os.path.join(root, file))
                 
    return jsonFiles

def writeAuthorInfo(filePointer,jsonLine):
    keys = []
    getKeys(jsonLine, keys)
    print(keys)

    authors = [] 
    altmetricId = -1
    mendeleyCount = 0
    totalPosts = 0

    for key in keys:
        value = jsonLine[key]
        print(key)
        if key == "citation" :
            citationKeys = []
            getKeys(jsonLine[key], citationKeys)
            for citationKey in citationKeys:
                if citationKey == "authors":
                    authors = jsonLine[key][citationKey]
        if key == "altmetric_id":
            altmetricId = jsonLine[key]

        if key == "counts":
            countKeys = []
            getKeys(jsonLine[key], countKeys)
            for countKey in countKeys:
                if countKey == "readers":
                    mendeleyCount = jsonLine[key][countKey]["mendeley"]
                    totalPosts = totalPosts + jsonLine[key][countKey]["mendeley"]
                    totalPosts = totalPosts + jsonLine[key][countKey]["connotea"]
                    totalPosts = totalPosts + jsonLine[key][countKey]["citeulike"]
                if countKey == "total":
                    totalPosts = totalPosts + jsonLine[key]["total"]["posts_count"]

    for author in authors:
        filePointer.write(''.join([author,",",str(altmetricId),","\
                ,str(mendeleyCount),",",str(totalPosts),"\n"]))
    
    print("Author file information:")
    print("alt_id",altmetricId,"mendeley",mendeleyCount,"totalPosts",totalPosts,\
            "authors",authors)

def buildCondensedDatabase(jsonFiles):
    print("Hello")

    filesProcessed = 0
    linesProcessed = 0

    # Files to write condensed data to
    
    # author, alt_id, mendeley, citeulike, connotea, total_posts
    authorInfo = open("E:\\School\\CSCI-641\\Data\\authorInfo.csv",'w+')
    authorInfo.truncate(0) # need '0' when using r+

    # twitter_id, twitter handle, twitter name, number of followers
    twitterInfo = open("E:\\School\\CSCI-641\\Data\\twitterInfo.csv",'w+')
    twitterInfo.truncate(0) # need '0' when using r+

    # altmetric_id, citation_id, citation_id, citation_id
    citationInfo = open("E:\\School\\CSCI-641\\Data\\citationInfo.csv",'w+')
    citationInfo.truncate(0) # need '0' when using r+

    # altmetric_id, type, #authors, list of authors separated by ',', FB_Post count, FB unique count, G+ post count, G+ unique user count, 
    # Twitter max followers, total followers, twitter post count, twitter unique users, list of twitter_id's separated by ','
    featureInfo = open("E:\\School\\CSCI-641\\Data\\featureInfo.csv",'w+')
    featureInfo.truncate(0) # need '0' when using r+

    
    for file in jsonFiles:
        filesProcessed = filesProcessed + 1
        with open(file) as json_file:
            linesProcessed = linesProcessed + 1
            for line in json_file:
                jsonLine = json.loads(line)
                writeAuthorInfo(authorInfo,jsonLine)
		        #writeAuthorInfo(authorInfo,jsonLine)
		        #writeAuthorInfo(authorInfo,jsonLine)
                #writeAuthorInfo(authorInfo,jsonLine)
    
    authorInfo.close()
    twitterInfo.close()
    citationInfo.close()
    featureInfo.close()
    
def main():
    print("Hello world!")
    """ Pattern for reading all files in the directory
    jsonFiles = findDataFiles(smallestSetPath)
    readAndPrintJsonFiles(jsonFiles)
    """
    oneJasonFile = []
    oneJasonFile.append("E:\\School\\CSCI-641\\real_limited\\23\\2300525.txt")
    #oneJasonFile.append("E:\\School\\CSCI-641\\tarfiles\\keys\\17\\1700000.txt")
    buildCondensedDatabase(oneJasonFile)

    #getProjectInfoFromJsonFiles(oneJasonFile)
    print("End of program")

if __name__ == '__main__':
    main()
