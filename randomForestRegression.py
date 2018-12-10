'''
Created on Dec 9, 2018

@author: brandon
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn import datasets
from sklearn.model_selection import train_test_split

from sklearn.ensemble import RandomForestRegressor
from sklearn.datasets import make_regression
from sklearn.ensemble import RandomForestClassifier

"""
    filePointer.write(''.join([str(altmetricId),",",str(mendeleyCount),",",str(readerCount),",",str(numAuthors),","]))
    filePointer.write(''.join([citationType,",",str(fbCounts),",",str(fbUniqueCount),",",str(googlePlusCount),",",str(googlePlusUniqueCount),","]))
    filePointer.write(''.join([str(twitterCount),",",str(twitterUniqueCount),",",str(maxFollowers),",",str(totalFollowers),","]))
    filePointer.write('\n')
"""

featureColumns=['ALmetId','MendeleyCount','ReaderCount','numAuthors','citatiionType', 'FbCounts','FbUniqueCount','G+Count','G+Unique','TwitterCount',\
               'twitterUniqueCount','TwitterMaxFollowers','TwitterTotalFollowers','blank']
"""
Paths to data
    fullDataSetPath = 'E:\School\CSCI-641\Data\fullDataSet\'
    limitedDataSetPath = 'E:\\School\\CSCI-641\\Data\\limitedDataSet\\featureInfoNoLists.csv'
    smallestSetPath = 'E:\\School\\CSCI-641\\Data\\smallestDataSet\\featureInfoNoLists.csv'
"""
fullDataSetPath = 'E:\\School\\CSCI-641\\Data\\fullDataSet\\featureInfoNoLists.csv'
limitedDataSetPath = 'E:\\School\\CSCI-641\\Data\\limitedDataSet\\featureInfoNoLists.csv'
smallestSetPath = 'E:\\School\\CSCI-641\\Data\\smallestDataSet\\featureInfoNoLists.csv'

pandaData = pd.read_csv(smallestSetPath,names=featureColumns,low_memory=False)

cols = pandaData.columns[pandaData.dtypes.eq('object')]
pandaData[cols] = pandaData[cols].apply(pd.to_numeric, errors='coerce')
pandaData = pandaData.replace(np.nan, 0)

print(pandaData[cols])

print(pandaData.dtypes)

inputs = pandaData['MendeleyCount']
#print(X)

target = pandaData.drop(['MendeleyCount'],axis=1)
#print(Y)

x_train, x_test, y_train, y_test = train_test_split(target,inputs,test_size=0.33)
print(len(x_train),len(y_train),len(x_test),len(y_test))


#print(y_train)

clf=RandomForestRegressor(random_state=0, n_estimators=100)

clf.fit(x_train,y_train)

y_pred=clf.predict(x_test)

print(y_pred, y_test)

#Import scikit-learn metrics module for accuracy calculation
from sklearn import metrics
# Model Accuracy, how often is the classifier correct?
#print("Accuracy:",metrics.accuracy_score(y_test, y_pred))

# logreg = LogisticRegression(C=1e5, solver='lbfgs', multi_class='multinomial')

# Create an instance of Logistic Regression Classifier and fit the data.
#logreg.fit(X, Y)

#data = pd.DataFrame(d1,columns=featureColumns)


def main():
    print("Hello world!")


if __name__ == '__main__':
    main()