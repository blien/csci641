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

def writeFeatureInfo(filePointer,jsonLine):
    keys = []
    getKeys(jsonLine, keys)

    citationIdList = []
    altmetricId = 0
    authors = []
    numAuthors = 0
    citationType = ''
    # socialMedia features
    fbCounts = 0
    fbUniqueCount = 0
    googlePlusCount = 0
    googlePlusUniqueCount = 0
    twitterCount = 0
    twitterUniqueCount = 0
    mendeleyCount = 0
    readerCount = 0
    maxFollowers = 0
    totalFollowers = 0
    twitterIds = []

    for key in keys:
        if key == "altmetric_id":
            altmetricId = jsonLine[key]
        if key == "citation":
            citationKeys = []
            getKeys(jsonLine[key], citationKeys)
            for citationKey in citationKeys:
                if citationKey == "authors":
                    authList = jsonLine[key][citationKey]
                    for auth in authList:
                        authors.append(auth)
                        numAuthors = numAuthors + 1
                if citationKey == "type":
                    citationType = jsonLine[key][citationKey]
        if key == "counts":
            countKeys = []
            getKeys(jsonLine[key], countKeys)
            for ck in countKeys:
                if ck == "twitter":
                    twitterCount = jsonLine[key][ck]["posts_count"]
                    twitterUniqueCount = jsonLine[key][ck]["unique_users_count"]
                if ck == "facebook":
                    googlePlusCount = jsonLine[key][ck]["posts_count"]
                    googlePlusUniqueCount = jsonLine[key][ck]["unique_users_count"]
                if ck == "googleplus":
                    fbCounts = jsonLine[key][ck]["posts_count"]
                    fbUniqueCount = jsonLine[key][ck]["unique_users_count"]
                if ck == "readers":
                    readerCount = readerCount + jsonLine[key][ck]["citeulike"]
                    readerCount = readerCount + jsonLine[key][ck]["connotea"]
                    readerCount = readerCount + jsonLine[key][ck]["mendeley"]
                    mendeleyCount = jsonLine[key][ck]["mendeley"]

        if key == "posts":
            postKeys = []
            getKeys(jsonLine[key], postKeys)
            for pk in postKeys:
                if pk == "twitter":
                    for obj in jsonLine[key][pk]:
                        authKeys = []
                        getKeys(obj, authKeys)
                        for k in authKeys:
                            if k == "author":
                                totalFollowers = totalFollowers + obj[k]["followers"]
                                if obj[k]["followers"] > maxFollowers:
                                    maxFollowers = obj[k]["followers"]
                                twitterIds.append(obj[k]["tweeter_id"])

    print("Feature info")
    print("numAuthors",citationType,mendeleyCount, readerCount,numAuthors,authors)
    print("socialMediaCounts",maxFollowers,totalFollowers,twitterCount,twitterUniqueCount,googlePlusCount,googlePlusUniqueCount,fbCounts,fbUniqueCount,twitterIds)

def writeCitationIdFile(filePointer,jsonLine):
    keys = []
    getKeys(jsonLine, keys)

    citationIdList = []
    altmetricId = 0

    for key in keys:
        if key == "altmetric_id":
            altmetricId = jsonLine[key]
        if key == "posts":
            postKeys = []
            getKeys(jsonLine[key], postKeys)
            for pKey in postKeys :
                for obj in jsonLine[key][pKey]:
                    objKeys = []
                    getKeys(obj,objKeys)
                    for objKey in objKeys:
                        if objKey == "citation_ids":
                            citationList = obj[objKey]
                            for citation in citationList:
                                citationIdList.append(citation)
    
    filePointer.write(''.join([str(altmetricId),","]))
    for citation in citationIdList:
        filePointer.write(''.join([str(citation),","]))
    
    filePointer.write("\n")

def writeTwitterInfo(filePointer,jsonLine):
    keys = []
    getKeys(jsonLine, keys)
    
    numFollowers = 0
    name = ''
    twitterId = 0
    twitterHandle = ''

    for key in keys:
        if key == "posts" :
            twitterKeys = []
            getKeys(jsonLine[key], twitterKeys)
            for twitterKey in twitterKeys:
                if twitterKey == "twitter":
                    for obj in jsonLine[key][twitterKey]:
                        #print(json.dumps(obj, indent = 4, sort_keys=True))
                        authKeys = []
                        getKeys(obj, authKeys)
                        for k in authKeys:
                            if k == "author":
                                name = obj[k]["name"]
                                twitterId = obj[k]["tweeter_id"]
                                twitterHandle = obj[k]["id_on_source"]
                                numFollowers = obj[k]["followers"]
                                name = name.encode("utf8")
                                twitterHandle = twitterHandle.encode("utf8")
                        #print("twitterFileInfo",twitterId,twitterHandle,numFollowers,name)
                        filePointer.write(''.join([str(twitterId),",",str(twitterHandle),",",str(name),",",str(numFollowers),"\n"]))

def writeAuthorInfo(filePointer,jsonLine):
    keys = []
    getKeys(jsonLine, keys)
    
    authors = [] 
    altmetricId = -1
    mendeleyCount = 0
    totalPosts = 0

    for key in keys:
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
    
    #print("Author file information:")
    #print("alt_id",altmetricId,"mendeley",mendeleyCount,"totalPosts",totalPosts,"authors",authors)

def buildCondensedDatabase(jsonFiles):
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
                writeTwitterInfo(twitterInfo,jsonLine)
                writeCitationIdFile(citationInfo,jsonLine)
                writeFeatureInfo(authorInfo,jsonLine)
    
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
