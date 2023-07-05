
from __future__ import unicode_literals
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from collections import Counter
import pandas as pd
import numpy as np



class Classifier():
    def __init__(self):
        #Multi label classifier
        forest = RandomForestClassifier(n_estimators=100, random_state=1)
        self.clf = MultiOutputClassifier(forest, n_jobs=-1)

    def fit(self, X, y):

        self.clf.fit(X, y)

    def predict(self, X):
        y_pred = np.array(self.clf.predict(X))
        return y_pred

    def predict_proba(self, X):
        raise NotImplemented
        """
        Compte the probailities for each label
        Important: this class needs to return an 2D array with 2 columns per label, so 109*2 columns. """
        proba = self.clf.predict_proba(X)
        #Proba is a list of size 109, one for each label, each element is an array of size n_samples * 2,
        #except some times when it is n_sample*1 so a little work is needed to reshape the array
        y_proba = proba[0]
        for x in proba[1 : ] :
            if x.shape[1] == 2 : 
                y_proba = np.hstack((y_proba,x))
            else:
                y_proba = np.hstack((y_proba,x,np.zeros_like(x)))
                             
        return y_proba
