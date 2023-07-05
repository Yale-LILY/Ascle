#%%
import itertools
import os
import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import MultiLabelBinarizer

from .utils.preprocessing import clean_data
from torchnlp.utils import lengths_to_mask
from .utils.BERTRunner import run_BERT, convertBERT
#%%
class codingPipeline:
    """Base class for the mimic icd9 classification pipeline"""
    def __init__(self, model='forest', data_path='../data/', text_col='TEXT', label_col='TARGET', verbose=True, bert_fast_dev_run=False, run=True):
        self.label_col=label_col
        self.text_col=text_col
        self.data_path = data_path
        self.prep_path = data_path + 'mimic_prep.csv'

        if model == 'BERT':
            self.model_type='BERT'
            if run:
                self.model = self.run_bert_model(bert_fast_dev_run)
        else:
            self.model_type='notBERT'
            if not os.path.exists(self.data_path):
                os.mkdir(self.data_path)
            if not os.path.exists(self.prep_path):
                df = self.make_preproc_data()
                self.df = df
            else:
                df = pd.read_csv(self.prep_path, converters={self.label_col: eval}, index_col=0)
            
            if run:
                self.run_model(df, model, verbose=verbose)

    def load_data(self):
        """Load in the processed data for testing"""
        df = pd.read_csv(self.prep_path, converters={self.label_col: eval}, index_col=0)
        self.data = df
        
    def run_bert_model(self, bert_fast_dev_run):
        """Helper function to run the bert model"""
        model = run_BERT(self.data_path, bert_fast_dev_run)
        self.model = model
        return model
    
    def predict(self, item):
        """Run trained model on datum"""
        if self.model_type =='BERT':
            tokens, masked_item = convertBERT(item)
            import torch
            device = torch.device("cuda")
            with torch.no_grad():
                preds = self.model(tokens.to(device), masked_item.to(device))
                preds = preds.detach().cpu().numpy()
                return np.argmax(preds, axis=1)
        if not isinstance(item, list):
            item = [item]
        item = self.vectorizer.transform(item)
        return self.mlBinarizer.inverse_transform(self.model.predict(item))

    def make_preproc_data(self):
        """Preprocess data"""
        df = pd.read_csv(self.data_path + 'mimic_full.csv', converters={self.label_col: eval})
        df[self.text_col] = clean_data(df[self.text_col])
        df.to_csv(self.data_path + 'mimic_prep.csv')
        return df

    def run_model(self, df, model, report=False, verbose=True):
        """Run a sklearn-based model"""
        X = self.vectorize(df[self.text_col])
        y = self.mlb(df[self.label_col])
        if model =='forest':
            self.model = RandomForestClassifier(n_jobs=-1)
        else:
            self.model = model
        X_train,X_test,y_train,y_test = train_test_split(X, y, test_size=0.3, random_state=123)

        self.model.fit(X_train, y_train)

        
        # test and predict
        y_pred = self.model.predict(X_test)

        # Classification metrics
        classification_report_test = classification_report(y_test, y_pred)
        self.auroc = roc_auc_score(y_test, y_pred)
        self.report = classification_report(y_test, y_pred, output_dict=True)
        # classification_report_train = classification_report(y_train, self.model.predict(X_train), output_dict=True)

        if verbose:
            print('\nClassification Report')
            print('======================================================')
            print('\n', classification_report_test)
    
                    
    def vectorize(self, series):
        """Helper function to vectorize features"""
        td = TfidfVectorizer(max_features=4500)
        transformed = td.fit_transform(series)
        self.vectorizer = td
        return transformed


    def mlb(self, labels):
        """Helper function to transform labels into an encoding schema
           using sklearns multi label binarizer"""
        all_labels = set(itertools.chain.from_iterable(labels))
        self.labels = all_labels
        mlBinarizer = MultiLabelBinarizer()
        mlBinarizer.fit([list(all_labels)])
        self.mlBinarizer = mlBinarizer
        return mlBinarizer.transform(labels)