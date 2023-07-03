import sys
import os
import torch
import re
import loader
# from allennlp.models.archival import *
from allennlp.data import DatasetReader
from allennlp.common.params import Params
from allennlp.predictors.text_classifier import TextClassifierPredictor
import time

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ehrkit import ehrkit
# from config import USERNAME, PASSWORD


def load_glove():
    # Loads GLOVE model
    glove_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glove_sentiment_predictor.txt")
    if os.path.exists(glove_path):  # same dir for github
        print('Loading Glove Sentiment Analysis Model')
        predictor = torch.load(glove_path)
    else:
        print('Downloading Glove Sentiment Analysis Model')
        predictor = loader.download_glove()
    return predictor


def load_roberta():
    # Loads Roberta model
    serialization_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roberta', '')
    config_file = os.path.join(serialization_dir, 'config.json')
    if os.path.exists(config_file):
        print('Loading Roberta Sentiment Analysis Model')
        model_file = os.path.join(serialization_dir, 'whole_model.pt')
        model = torch.load(model_file)
        loaded_params = Params.from_file(config_file)
        dataset_reader = DatasetReader.from_params(loaded_params.get('dataset_reader'))

        # Gets predictor from model and dataset reader
        predictor = TextClassifierPredictor(model, dataset_reader)

        # weights_file = os.path.join(serialization_dir, 'weights.th')
        # loaded_model = Model.load(loaded_params, serialization_dir, weights_file) # Takes forever
        # archive = load_archive(os.path.join('roberta', 'model.tar.gz')) # takes forever
    else:
        print('Downloading Roberta Sentiment Analysis Model')
        predictor = loader.download_roberta()
    return predictor


def get_doc():
    doc_id = input("MIMIC Document ID [press Enter for random]: ")
    if doc_id == '':
        ehrdb.cur.execute("SELECT ROW_ID FROM mimic.NOTEEVENTS ORDER BY RAND() LIMIT 1")
        doc_id = ehrdb.cur.fetchall()[0][0]
        print('Document ID: %s' % doc_id)
    try:
        text = ehrdb.get_document(int(doc_id))
        clean_text = re.sub('[^A-Za-z0-9\.\,\-\/]+', ' ', text).lower()
        return doc_id, clean_text
    except:
        message = 'Error: There is no document with ID \'' + doc_id + '\' in mimic.NOTEEVENTS'
        sys.exit(message)


if __name__ == '__main__':
    # ehrdb = ehrkit.start_session(USERNAME, PASSWORD)
    ehrdb = ehrkit.start_session("jeremy.goldwasser@localhost", "mysql4710")
    doc_id, clean_text = get_doc()
    # print('LENGTH OF DOCUMENT: %d' % len(clean_text))

    x = input('GloVe or RoBERTa predictor [g=GloVe, r=RoBERTa]? ')
    if x == 'g':
        glove_predictor = load_glove()
        probs = glove_predictor.predict(clean_text)['probs']
    elif x == 'r':
        roberta_predictor = load_roberta()
        try:
            probs = roberta_predictor.predict(clean_text)['probs']
        except:
            print('Document too long for RoBERTa model. Using GLoVe instead.')
            glove_predictor = load_glove()
            probs = glove_predictor.predict(clean_text)['probs']
    else:
        sys.exit('Error: Must input \'g\' or  \'r\'')

    classification = 'Positive' if probs[0] >= 0.5 else 'Negative'
    print('Sentiment of document: %s' % classification)


    # # jeremy.goldwasser@localhost
    # # Save sentiment as json file
    # sentiment = {'text': clean_text, 'sentiment': classification, 'prob': probs[0]}
    # with open('predicted_sentiments/' + str(doc_id) + '.json', 'w', encoding='utf-8') as f:
    #     json.dump(sentiment, f, ensure_ascii=False, indent=4)

