'''
Created on Dec 2, 2018

@author: brandon
'''

import sys
import scipy as sp
import numpy as np
import pandas as pd

printOutput = False

fullDataSetPath = 'E:\\School\\CSCI-641\\tarfiles\\keys'
limitedDataSetPath = 'E:\\School\\CSCI-641\\data_limited'
smallestSetPath = 'E:\\School\\CSCI-641\\real_limited'
socialColumns=['FbCount','FbUniqueUsrCount','TwitterCount','TwitterUniqueUsrCount','TotalPosts', 'TwitterAuthorInfo']

# set panda options
#pd.set_option('display.max_rows', 1000)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

def main():

    print("Hello world!")
    """ 
    Read CSV file - remove all lines where fb count, twitter count, g+ count && mendeley count == 0
    """
    numLines = 0
    numOutputLines = 0

    inputFilePath = "E:\\School\\CSCI-641\\Data\\fullDataSet\\featureInfoNoLists.csv"
    outputFilePath = "E:\\School\\CSCI-641\\Data\\fullDataSet\\featureInfoNoListsReduced.csv"

    #inputFile = open(inputFilePath,'r+')
    outputFile = open(outputFilePath,'w+')
    outputFile.truncate(0) # need '0' when using r+

    featureColumns=['AltmetId','MendeleyCount','ReaderCount','numAuthors','citationType', 'FbCounts','FbUniqueCount','G+Count','G+Unique','TwitterCount',\
               'twitterUniqueCount','TwitterMaxFollowers','TwitterTotalFollowers','blank']

    df = pd.read_csv(inputFilePath, header = None,names = featureColumns,low_memory=True)
    
    newFrame = pd.DataFrame(columns=featureColumns)

    count = 0
    rowCount = df['AltmetId'].count()
    print("rowCount",rowCount)
    print(np.shape(df))

    data = {}
    dataIndex = 0
    for index, row in df.iterrows():
        count = count + 1
        if count % 10000 == 0:
            print (count, ((count/rowCount)*100))

        if row['MendeleyCount'] == 0 and row['FbCounts'] == 0 and  row['G+Count'] == 0 and row['TwitterCount'] == 0 :
            #newFrame.loc[dataIndex] = row
            for col in featureColumns:
                if col != 'blank':
                    outputFile.write(''.join([str(row[col]),","]))
                if col == 'blank':
                    outputFile.write("\n")
            #newFrame.append(row,ignore_index=True)
            #data[dataIndex] = row[featureColumns]
            #dataIndex = dataIndex + 1
        if  row['FbCounts'] != 0 or row['G+Count'] != 0 or row['TwitterCount'] != 0 :
            for col in featureColumns:
                if col != 'blank':
                    outputFile.write(''.join([str(row[col]),","]))
                if col == 'blank':
                    outputFile.write("\n")
            #newFrame.loc[dataIndex] = row
    outputFile.close()
            #data[dataIndex] = row[featureColumns]
            #dataIndex = dataIndex + 1
    """
    print(np.shape(df))
    print(np.shape(newFrame))
   # print(newFrame)
    #newFrame.to_csv(outputFilePath)
    """

    print("End of program")

if __name__ == '__main__':
    main()
