# Functions for extracting features from text
# Mostly taken from https://github.com/rachitjain2706/Auto-Text-Summarizer
import re
import os
import time
from math import log
import sys
import shutil
import traceback
import json
from collections import Counter

import nltk
from nltk.corpus import stopwords


# Stores number of nouns, average tf*ISF score, # in document, and length
class Sentence:
    def setSentenceParams(self, n_nouns, avg_tfisf, sno):
        self.n_nouns = n_nouns
        self.avg_tfisf = avg_tfisf
        self.sno = sno

    def setSentLen(self, slen):
        self.slen = slen


# Make list of words, only characters kept
def sentence_to_wordlist(raw):
    clean = re.sub("[^a-zA-Z]", " ", raw)
    words = clean.split()
    return words


# Stopword removal
def remove_stopwords(tokens):
    cleaned_tokens = []
    stop_words = stopwords.words('english')
    for token in tokens:
        cleaned_tokens_sentence = []
        for word in token:
            if word not in stop_words:
                cleaned_tokens_sentence.append(word)
        cleaned_tokens.append(cleaned_tokens_sentence)
    return cleaned_tokens


def ISF(N, n):
    '''N : total number of sentences in corpus
       n : number of sentences with our word in it'''
    if n > 0:
        return float(log(float(N) / n) + 1)
    else:# This happens once
        return float(log(float(N) / 2) + 1)


def seconds(x):
    s_day = 60 * 60 * 24
    s_hour = 60 * 60
    s_min = 60

    n_days = x // s_day
    n_hours = (x - (s_day * n_days)) // s_hour
    n_mins = (x - (s_day * n_days) - (s_hour * n_hours)) // s_min
    n_secs = x - (s_day * n_days) - (s_hour * n_hours) - (s_min * n_mins)
    return n_days, n_hours, n_mins, n_secs


def make_tfisf_dict(raw_sentences, raw_data, freq):
    n_sents = len(raw_sentences)  # This is our N
    unique_words = set(raw_data.split())

    final_list = []
    sent_occurrence_counter = 0
    # calculating number of sentences with our word in it
    count = 0
    stop_words = stopwords.words('english')
    for unq_word in unique_words:
        if unq_word not in stop_words:
            for sent in raw_sentences:
                for word in sent.split():
                    if unq_word == word:
                        sent_occurrence_counter += 1
                        break
            final_list.append([unq_word, freq[unq_word] * ISF(n_sents, sent_occurrence_counter)])
            sent_occurrence_counter = 0
            count += 1
    isf_dict = {}

    for word in final_list:
        isf_dict[word[0]] = word[1]
    return isf_dict


def sent_rank(cleaned_tokens, pos_array, isf_dict):
    sentNum = 0
    all_sentences = []
    max_avg_tfisf = -1
    max_nNouns = -1
    max_sentLen = -1
    for sent in cleaned_tokens:
        tempSent = Sentence()
        sentNum += 1
        tfisf = 0
        pos = 0
        for word in sent:
            if word in pos_array:
                pos_val = pos_array[word]
                if pos_val == 'NNP' or pos_val == 'NNPS':
                    pos += 1
                if word in isf_dict:
                    tfisf += isf_dict[word]
        if len(sent) > 0:
            avg_tfisf = float(tfisf) / len(sent)
        else:
            avg_tfisf = 0

        if avg_tfisf > max_avg_tfisf:  # For normalizing
            max_avg_tfisf = avg_tfisf

        if pos > max_nNouns:  # For normlizing
            max_nNouns = pos

        if len(sent) > max_sentLen:
            max_sentLen = len(sent)

        tempSent.setSentenceParams(float(pos), avg_tfisf, sentNum)
        tempSent.setSentLen(float(len(sent)))
        all_sentences.append(tempSent)

    return all_sentences, max_avg_tfisf, max_nNouns, max_sentLen


def normalize(all_sentences, max_avg_tfisf, max_nNouns, max_sentLen):
    for sentence in all_sentences:
        if max_avg_tfisf > 0:
            sentence.avg_tfisf /= max_avg_tfisf
        if max_nNouns > 0:
            sentence.n_nouns /= max_nNouns
        if max_sentLen > 0:
            sentence.slen /= max_sentLen
    return all_sentences


def build_vecs(text, summary, tokenizer):
    # Tokenize all text into sentences
    raw_sentences = tokenizer.tokenize(text)
    # # Separate sentences by newline chars
    # raw_sentences = []
    # for sent in raw_sentences_unclean:
    #     split = sent.split("\n")
    #     for i in split:
    #         if len(i) > 0:
    #             raw_sentences.append(i)
    # print("Done tokenizing")

    # Makes each sentence a list of cleaned words
    tokens = []
    for raw_sentence in raw_sentences:
        tokens.append(sentence_to_wordlist(raw_sentence))

    # Removal of stop words
    cleaned_tokens = remove_stopwords(tokens)

    # Removal of not real words for Counter (leaving in harmless stop words)
    cleaned_raw_data = sentence_to_wordlist(text)

    # Counts term frequency for all words
    freq = Counter(cleaned_raw_data)
    # print("Done term freq")

    # Make tf-isf dict of (word, tf*ISF) pairs
    isf_dict = make_tfisf_dict(raw_sentences, text, freq)
    # print("Done making tfisf dict")

    # Do POS Tagging (each word only tagged once)
    pos_data = nltk.pos_tag(cleaned_raw_data)
    pos_array = {}
    for word in pos_data:
        pos_array[word[0]] = word[1]
    # print("Done with POS tagging")

    # Calculates feature vectors for each sentence then normalizes
    all_sentences, max_avg_tfisf, max_nNouns, max_sentLen = sent_rank(cleaned_tokens, pos_array, isf_dict)
    all_sentences = normalize(all_sentences, max_avg_tfisf, max_nNouns, max_sentLen)

    # Makes input features
    features = []
    for sentence in all_sentences:
        features.append([sentence.avg_tfisf, sentence.n_nouns, sentence.slen])
    # print("Done w feature vecs")
    if not summary:
        # Only interested in input feature extraction
        return features, None

    # Tokenizes summary into sentences
    raw_summaries = tokenizer.tokenize(summary)
    # print("Done tokenizing summaries")

    # A zero for every sentence in raw_sentences. Fills with 1's wherever sentence is in summary
    outputs = [0 for _ in range(len(raw_sentences))]
    index = 0
    for raw_sentence in raw_sentences:
        if len(raw_sentence) > 0 and raw_sentence != '.':
            for summary_sentence in raw_summaries:
                if len(summary_sentence) > 0 and summary_sentence != '.':
                    if summary_sentence == raw_sentence:
                        # This sentence is one of the summary sentences
                        outputs[index] = 1
                        break
        index += 1
    # print("Done making classification vec")
    return features, outputs


def get_pubmed_nb_data(PARSED_DIR, NB_DIR, n_train, whole_body):
    os.mkdir(NB_DIR)
    os.mkdir(os.path.join(NB_DIR, 'test_json'))
    try:
        # Read selected Pubmed filenames
        EXS_DIR = os.path.dirname(NB_DIR)
        with open(os.path.join(EXS_DIR, 'training_files.txt'), 'r') as train:
            training_file_names = train.read().splitlines()
        with open(os.path.join(EXS_DIR, 'test_files.txt'), 'r') as test:
            test_file_names = test.read().splitlines()

        n_test = len(test_file_names)
        n_total = n_train + n_test
        train_features = []
        train_classes = []
        test_features = []
        test_classes = []
        if n_train >= 1000 and not whole_body:
            verbose = True
        elif n_train >= 200 and whole_body:
            verbose = True
        else:
            verbose = False
        start_time = time.time()
        for i in range(n_total):
            if i < n_train:
                filename = training_file_names[i]
            else:
                filename = test_file_names[n_train - i]
            with open(os.path.join(PARSED_DIR, 'abstract', filename + '.tgt'), 'r') as abs:
                abs_text = abs.read().replace('\n', '. ').replace('..', '.')
            with open(os.path.join(PARSED_DIR, 'merged', filename + '.mgd'), 'r') as mgd:
                mgd_text = mgd.read().replace('\n', '. ').replace('..', '.')

            # Builds feature vectors for sentences of that article
            tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
            features, classes = build_vecs(mgd_text, abs_text, tokenizer)

            # Adds to list
            if i < n_train:
                train_features.extend(features)
                train_classes.extend(classes)
            else:
                test_features.extend(features)
                test_classes.extend(classes)

            if verbose:
                # Update every 10 percent
                if i % round(n_total / 10) == 0 and i > 0:
                    elapsed = time.time() - start_time
                    exp_total = (elapsed / (i + 1)) * n_total
                    pct_complete = round((i / round(n_total / 10)) * 10)
                    pct_complete_train = min(round((i / round(n_train / 10)) * 10), 100)
                    pct_complete_test = max(round(((i - n_train) / round(n_test / 10)) * 10), 0)
                    print('{}% complete: {}% with train and {}% with test'
                          .format(pct_complete, pct_complete_train, pct_complete_test))
                    print('Estimated time remaining: '
                          '%d days, %d hours, %d minutes, %d seconds' % seconds(exp_total - elapsed))

            # Writes feature vectors to json file
            if i >= n_train:
                test_data = {'features': features, 'outputs': classes}
                path = os.path.join(NB_DIR, 'test_json', filename + '.json')
                with open(path, 'w') as f:
                    json.dump(test_data, f)

        # Saves feature and output lists to json
        all_data = {'train_features': train_features, 'train_outputs': train_classes,
                    'test_features': test_features, 'test_outputs': test_classes}
        json_path = os.path.join(NB_DIR, 'feature_vecs.json')
        with open(json_path, 'w') as f:
            json.dump(all_data, f)
    except Exception:
        shutil.rmtree(NB_DIR)
        traceback.print_exc()
        sys.exit('Deleting created Naive Bayes directories.')
    except KeyboardInterrupt:
        shutil.rmtree(NB_DIR)
        sys.exit('Keyboard Interrupt. Deleting created Naive Bayes directories.')

