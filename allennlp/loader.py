from allennlp.predictors.predictor import Predictor
from allennlp.predictors.text_classifier import TextClassifierPredictor
from allennlp.predictors.sentence_tagger import SentenceTaggerPredictor

from allennlp.models.archival import *
from allennlp.data import DatasetReader
from allennlp.common.params import Params
from allennlp.models import Model
import allennlp_models.classification
import allennlp_models.tagging

import torch
import os
import shutil


def rm_tmp(tmp_start):
    # Remove new directories in tmp
    tmp_now = os.listdir('/tmp')
    for i in tmp_now:
        if i not in tmp_start:
            print('removing directory /tmp/' + i)
            shutil.rmtree('/tmp/' + i)


def get_config(archive_path):
    archive = load_archive(archive_path)
    config = archive.config.duplicate()
    return config


def download_glove():
    # Saves TextClassifierPredictor object
    tmp_start = os.listdir('/tmp')
    glove_predictor = Predictor.from_path("https://storage.googleapis.com/allennlp-public-models/basic_stanford_sentiment_treebank-2020.06.09.tar.gz")
    glove_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'glove_sentiment_predictor.txt')
    torch.save(glove_predictor, glove_path)
    try:
        rm_tmp(tmp_start)
    except:
        pass
    return glove_predictor


def download_roberta():
    tmp_start = os.listdir('/tmp')
    archive_path = "https://storage.googleapis.com/allennlp-public-models/sst-roberta-large-2020.06.08.tar.gz"
    config = get_config(archive_path)
    roberta_predictor = Predictor.from_path(archive_path)

    serialization_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'roberta', '')
    if os.path.exists(serialization_dir):
        shutil.rmtree(serialization_dir)
    os.makedirs(serialization_dir)

    # Create config and model files
    config.to_file(os.path.join(serialization_dir, 'config.json'))
    with open(os.path.join(serialization_dir, 'whole_model.pt'), 'wb') as file:
        torch.save(roberta_predictor._model, file)

    try:
        rm_tmp(tmp_start)
    except:
        pass
    return roberta_predictor


def download_ner():
    tmp_start = os.listdir('/tmp')
    archive_path = "https://storage.googleapis.com/allennlp-public-models/ner-model-2020.02.10.tar.gz"
    config = get_config(archive_path)
    ner_predictor = Predictor.from_path(archive_path)

    serialization_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'elmo-ner', '')
    if os.path.exists(serialization_dir):
        shutil.rmtree(serialization_dir)
    os.makedirs(serialization_dir)

    config.to_file(os.path.join(serialization_dir, 'config.json'))
    vocab = ner_predictor._model.vocab
    vocab.save_to_files(os.path.join(serialization_dir, 'vocabulary'))
    with open(os.path.join(serialization_dir, 'whole_model.pt'), 'wb') as file:
        torch.save(ner_predictor._model.state_dict(), file)

    try:
        rm_tmp(tmp_start)
    except:
        pass
    return ner_predictor


def load_glove():
    # Loads GLOVE model
    glove_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "glove_sentiment_predictor.txt")
    if os.path.exists(glove_path):  # same dir for github
        print('Loading Glove Sentiment Analysis Model')
        predictor = torch.load(glove_path)
    else:
        print('Downloading Glove Sentiment Analysis Model')
        predictor = download_glove()
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
    else:
        print('Downloading Roberta Sentiment Analysis Model')
        predictor = download_roberta()
    return predictor


def load_ner():
    serialization_dir = "../allennlp/elmo-ner"

    config_file = os.path.join(serialization_dir, 'config.json')
    weights_file = os.path.join(serialization_dir, 'whole_model.pt')
    loaded_params = Params.from_file(config_file)
    loaded_model = Model.load(loaded_params, serialization_dir, weights_file)
    dataset_reader = DatasetReader.from_params(loaded_params.get('dataset_reader'))

    predictor = SentenceTaggerPredictor(loaded_model, dataset_reader)
    return predictor

if __name__ == "__main__":
    download_glove()
    download_roberta()
    download_ner()

