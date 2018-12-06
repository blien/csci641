'''
Created on Dec 2, 2018

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

fullDataSetPath = 'E:\\School\\CSCI-641\\tarfiles\\keys'
limitedDataSetPath = 'E:\\School\\CSCI-641\\data_limited'
smallestSetPath = 'E:\\School\\CSCI-641\\real_limited'
socialColumns=['FbCount','FbUniqueUsrCount','TwitterCount','TwitterUniqueUsrCount','TotalPosts', 'TwitterAuthorInfo']
postsColumns = ['followers', 'id_on_source', 'name','posted_on','rt_ids']

def get_keys(dl, keys_list):
    if isinstance(dl, dict):
        keys_list += dl.keys()
        map(lambda x: get_keys(x, keys_list), dl.values())
    elif isinstance(dl, list):
        map(lambda x: get_keys(x, keys_list), dl)

def findDataFiles(startingDir):
    print(startingDir)
    jsonFiles = []
    for root, dirs, files in os.walk(startingDir):
        for file in files:
            if file.endswith(".txt"):
                jsonFiles.append(os.path.join(root, file))
                #print(os.path.join(root, file))
                 
    return jsonFiles

def getAuthors(json_obj):
    authors = []
    keys = []
    get_keys(json_obj, keys)
    for key in keys:
        if key == "authors":
            authors = json_obj[key]

            #print(authors)
    
    return authors

def getPostInfo(json_obj):
    post_keys = []
    counts = [None] * 4
    
    """
    posts, twitter, author
                    id_on_source
                    name
                    tweeter id
    """
    
    get_keys(json_obj, post_keys)
    for key in post_keys :
        if key == "facebook":
            twKeys = []
            get_keys(json_obj[key], twKeys)
            for twKey in twKeys:
                if twKey == 'author':
                    authKeys = []
                    get_keys(json_obj[key][twKey],authKeys)
                    for authKey in authKeys:
                        if authKey == "followers":
                            print("")
                            if authKey == "id_on_source":
                                print("")
                            if authKey == "name":
                                print("")
            print("facebook")
        if key == "twitter":
            print("twitter!")

    return counts

def getSocialMediaInformation(json_obj, pandaFrame):
    post_keys = []
    # fb unique user count, fb post count, twitter unique user count, twitter post count, total posts
    counts = [0] * 5
    twitterUsers = []
    get_keys(json_obj, post_keys)
    
    for key in post_keys :
        if key == "facebook":
            fbKeys = []
            get_keys(json_obj[key], fbKeys)
            for fbKey in fbKeys :
                if fbKey == "unique_users_count":
                    counts[0] = json_obj[key][fbKey]
                if fbKey == "posts_count":
                    counts[1] = json_obj[key][fbKey]

        if key == "twitter":
            twKeys = []
            get_keys(json_obj[key], twKeys)
            for twKey in twKeys:
                if twKey == "posts_count":
                    counts[2] = json_obj[key][twKey]
                if twKey == "unique_users_count":
                    counts[3] = json_obj[key][twKey]
                if twKey == "unique_users":
                    twitterUsers = json_obj[key][twKey]

        if key == "total":
            totKeys = []
            get_keys(json_obj[key], totKeys)
            for totKey in totKeys:
                if totKey == "posts_count":
                    counts[4] = json_obj[key][totKey]
                    
    d1 = [[counts[0],counts[1],counts[2],counts[3],counts[4],twitterUsers]]

    data = pd.DataFrame(d1,columns=socialColumns)
    pandaFrame = pandaFrame.append(data)
    
    # print("Counts: ", counts)
    # print("TwitterUsers: ", twitterUsers)
    # print("Data", data)
    # print("Data\n",data)
    # print("PandaFrame:\n",pandaFrame)
    return pandaFrame


def getTwitterPosterList(json_obj):
    print("hi")

def recursivelyTraverseJson(json_obj):
    authors = []
    
    #Twitter author info is a map of author and followers
    socialMediaInfo = pd.DataFrame(columns=socialColumns)

    keys = []
    get_keys(json_obj, keys)
    print(keys)

    for key in keys:
        value = json_obj[key]
        if key == "posts" :
            getPostInfo(json_obj[key])
            #for pkey in post_keys:
                #if(pkey == "twitter"):
                   #print(pkey, json_obj[key][pkey])
        if key == "counts" :
            socialMediaInfo = getSocialMediaInformation(json_obj[key],socialMediaInfo)

            # get counts facebook post count, unique user count, twitter post count, twitter unique user
        if key == "citation" :
            print("found citations")
            authors = getAuthors(json_obj[key])
 
            #print(authors)
        #if isinstance(value, dict) or isinstance(value, list):
        #    recursivelyTraverseJson(value)
 

    """ print authors
    for auth in authors:
        print(auth.encode('utf-8'))
    """
    print("SocialMediaInfo\n",socialMediaInfo)
    print("write all info to csv file")

def getProjectInfoFromJsonFiles (jsonFiles):
    json_data = []
    filesProcessed = 0
    linesProcessed = 0
    for file in jsonFiles:
        filesProcessed = filesProcessed + 1
        with open(file) as json_file:
            print("processing: " + file)
            for line in json_file:
                #print(line)
                linesProcessed = linesProcessed + 1
                cur_json = json.loads(line)
                json_data.append(cur_json)

                """
                below code gets altmetric keys/information
                """
                
                recursivelyTraverseJson(cur_json)
                """
                keys = []
                get_keys(cur_json, keys)
                print(keys)
                """    
                    
    print("finished reading json files")
    print("files: " + str(filesProcessed))
    print("lines: " + str(linesProcessed))
    return json_data


def readAndPrintJsonFiles (jsonFiles):
    json_data = []
    filesProcessed = 0
    linesProcessed = 0
    for file in jsonFiles:
        filesProcessed = filesProcessed + 1
        with open(file) as json_file:
            print("processing: " + file)
            for line in json_file:
                #print(line)
                linesProcessed = linesProcessed + 1
                cur_jason = json.loads(line)
                json_data.append(cur_jason)
                
                print (json.dumps(cur_jason, indent = 4, sort_keys=True))

                """
                below code gets altmetric keys/information
                """
                #keys = []
                #get_keys(cur_jason, keys)
                #print(keys) 
    print("finished reading json files")
    print("files: " + str(filesProcessed))
    print("lines: " + str(linesProcessed))
    return json_data

def main():
    print("Hello world!")
    """ Pattern for reading all files in the directory
    jsonFiles = findDataFiles(smallestSetPath)
    readAndPrintJsonFiles(jsonFiles)
    """
    oneJasonFile = []
    oneJasonFile.append("E:\\School\\CSCI-641\\tarfiles\\keys\\17\\1700000.txt")
    getProjectInfoFromJsonFiles(oneJasonFile)
    print("End of program")

if __name__ == '__main__':
    main()
    
    
    
"""
if value :
    if not isinstance(value, dict) and not isinstance(value, list):
        if isinstance(value, str):
            print(key, value.encode('utf-8'))
        else :
            print(type(value))
            print(key, value)
else:
    recursivelyTraverseJson(value)
"""