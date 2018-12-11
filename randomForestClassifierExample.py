'''
Created on Dec 10, 2018

@author: brandon
'''
#Importing Libraries]
from numpy.polynomial.tests.test_classes import classes


"""
1.) Import libraries
"""
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.externals import joblib
from sklearn.metrics import precision_recall_fscore_support

from sklearn.metrics import precision_score, \
    recall_score, confusion_matrix, classification_report, \
    accuracy_score, f1_score


print('Libraries Imported')

# set panda options
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


"""
2.) Get dataset
"""
#Creating Dataset and including the first row by setting no header as input
dataset = pd.read_csv('iris.data.csv', header = None)
#Renaming the columns
dataset.columns = ['sepal length in cm', 'sepal width in cm','petal length in cm','petal width in cm','species']
print('Shape of the dataset: ' + str(dataset.shape))
print(dataset.head())

"""
3.) Create dpendent variable classes

    TODO: change mendeley values to [0-33 percentile,33-66 percentile, above 66 percentile]
"""

#Creating the dependent variable class
factor = pd.factorize(dataset['species'])
dataset.species = factor[0]
definitions = factor[1]
print(dataset.species.head())
print(definitions)

"""
4.) Extracting features and output
"""
#Splitting the data into independent and dependent variables
X = dataset.iloc[:,0:4].values
y = dataset.iloc[:,4].values
print('The independent features set: ')
print(X[:5,:])
print('The dependent variable: ')
print(y[:5])

print(y)

"""
5.) Split data to training/testing using train_test_split
"""
# Creating the Training and Test set from data
X_train, X_test, y_train, y_test = train_test_split(X[1:,], y[1:,], test_size = 0.25, random_state = 21)

print(np.shape(X_train))
#print(X_train[1:,])
"""
6.) Feature Scaling
"""

# Feature Scaling
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

"""
7.) Training the Model
"""
# Fitting Random Forest Classification to the Training set
classifier = RandomForestClassifier(n_estimators = 10, criterion = 'entropy', random_state = 42)
classifier.fit(X_train, y_train)

"""
8.) Evaluating the performance
"""

# Predicting the Test set results
y_pred = classifier.predict(X_test)
#Reverse factorize (converting y_pred from 0s,1s and 2s to Iris-setosa, Iris-versicolor and Iris-virginica
reversefactor = dict(zip(range(3),definitions))
y_test = np.vectorize(reversefactor.get)(y_test)
y_pred = np.vectorize(reversefactor.get)(y_pred)
# Making the Confusion Matrix
print(pd.crosstab(y_test, y_pred, rownames=['Actual Species'], colnames=['Predicted Species']))

print ('Accuracy:', accuracy_score(y_test, y_pred))
print ('F1 score:', f1_score(y_test, y_pred,average=None))
print ('Recall:', recall_score(y_test, y_pred,average=None))
print ('Precision:', precision_score(y_test, y_pred,average=None))
print ('\n clasification report:\n', classification_report(y_test,y_pred))
print ('\n confussion matrix:\n',confusion_matrix(y_test, y_pred))

print("End")
"""
9.) Storing the trained model

print(list(zip(dataset.columns[0:4], classifier.feature_importances_)))
joblib.dump(classifier, 'randomforestmodel.pkl') 
"""

