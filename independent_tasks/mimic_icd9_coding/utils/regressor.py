
from __future__ import unicode_literals
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
import pandas as pd
import numpy as np



class Regressor():
    def __init__(self):
        #self.raw_embedding = load_embedding_from_url(url='http://nlp.stanford.edu/data/glove.6B.zip', filename='glove.6B.200d.txt')
        self.clf = RandomForestClassifier()
        # self.metaclf = XGBClassifier()
    def fit(self, X, y):

        self.clf.fit(X, y)


    def predict(self, X):
        proba = self.clf.predict_proba(X)
        res = []
        for x in proba:
            temp = []
            for i,y in enumerate(x):
                if y[0] == 1.:
                    temp.append(0)
                else:
                    temp.append(1)
            res.append(temp)
        y_proba = np.array(res).T
        return 0.1 * np.ones_like(y_proba)