from __future__ import unicode_literals
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import unicodedata
import pandas as pd
import numpy as np
import string
import re
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

stemmer = SnowballStemmer('english')
stpwrds = set([stopword for stopword in stopwords.words('english')])
stpwrds.update({'admission', 'birth', 'date', 'discharge', 'service','sex'})
punct = set(string.punctuation.replace('-', ''))
punct.update(["``", "`", "..."])

def clean_text_simple(text, my_stopwords=stpwrds, punct=punct, remove_stopwords=True, stemming=False):
    text = text.lower()
    text = ''.join(l for l in text if l not in punct) # remove punctuation (preserving intra-word dashes)
    text = re.sub(' +',' ',text) # strip extra white space
    text = text.strip() # strip leading and trailing white space 
    tokens = text.split() # tokenize (split based on whitespace)
    tokens = [w for w in tokens if w.isalpha()]
    tokens = [w for w in tokens if len(w) > 2]

    if remove_stopwords:
        # remove stopwords from 'tokens'
        tokens = [x for x in tokens if x not in my_stopwords]

    if stemming:
        # apply stemmer
        stemmer = SnowballStemmer('english')
        tokens = [stemmer.stem(t) for t in tokens]

    return tokens



def document_preprocessor(doc):
    # TODO: is there a way to avoid these encode/decode calls?
    try:
        doc = unicode(doc, 'utf-8')
    except NameError:  # unicode is a default on python 3
        pass
    doc = unicodedata.normalize('NFD', doc)
    doc = doc.encode('ascii', 'ignore')
    doc = doc.decode("utf-8")
    return str(doc)

class FeatureExtractor(TfidfVectorizer):
    """Convert a collection of raw docs to a matrix of TF-IDF features. """

    def __init__(self):
        self.min_occur = 1
        self.tfidf = TfidfVectorizer(ngram_range=(1, 1))
        self.vocab = Counter()
        super(FeatureExtractor, self).__init__(
                analyzer='word',stop_words ='english', preprocessor=document_preprocessor)

    def fit(self, X_df, y=None):
        """Learn a vocabulary dictionary of all tokens in the raw documents.

        Parameters
        ----------
        X_df : pandas.DataFrame
            a DataFrame, where the text data is stored in the ``TEXT``
            column.
        """
        statements = pd.Series(X_df).apply(clean_text_simple)
        self.vocab = Counter()
        for statement in statements:
            self.vocab.update(statement)   
        tokens = [k for k,c in self.vocab.items() if c >= self.min_occur]      
        statements = statements.apply(lambda x: [w for w in x if w in tokens])
        statements = statements.apply(lambda x: ' '.join(x))
        statements = list(statements.values)
        self.tfidf.fit(statements)
        return self

    def fit_transform(self, X_df, y=None):
        
        self.fit(X_df)
        return self.transform(self.X_df)

    def transform(self, X_df):

        statements = pd.Series(X_df.TEXT).apply(clean_text_simple)
        tokens = [k for k,c in self.vocab.items() if c >= self.min_occur]      
        
        statements = statements.apply(lambda x: [w for w in x if w in tokens])
        statements = statements.apply(lambda x: ' '.join(x))
        statements = list(statements.values)
        X_fe=self.tfidf.transform(statements)
        return X_fe
