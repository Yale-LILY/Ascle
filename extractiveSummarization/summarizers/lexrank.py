'''
Derived from https://github.com/crabcamp/lexrank/blob/dev/lexrank/lexrank.py

MIT License

Copyright (c) 2018 Ocean S.A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import math
import numpy as np  
import pandas as pd 
import re   

from collections import Counter, defaultdict
from scipy.sparse.csgraph import connected_components
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords

PUNCTUATION_SIGNS = set('.,;:¡!¿?…⋯&‹›«»\"“”[]()⟨⟩}{/|\\')


class Lexrank:
    def __init__(self, documents, stop_words=None, threshold=.03, include_new_words=True):
        if not stop_words:
            self.stopwords = set(stopwords.words('english'))
        else:
            self.stopwords = stop_words
        self.threshold = threshold
        self.include_new_words = include_new_words
        self.idf_score = self._calc_idf(documents)
        
    def get_summary(self, sentences, summary_size=1):
        if not isinstance(summary_size, int) or summary_size < 1:
            raise ValueError('summary_size should be a positive integer')

        lex_scores = self.rank_sentences(sentences)
        sorted_ix = np.argsort(lex_scores)[::-1]
        summary = [sentences[i] for i in sorted_ix[:summary_size]]

        return summary

    def rank_sentences(self, sentences):
        tf_scores = [
            Counter(self.tokenize_into_words(sentence)) for sentence in sentences
        ]

        sim_matrix = self._calc_sim_matrix(tf_scores)

        scores = degree_centrality_scores(sim_matrix, threshold=self.threshold)
        return scores

    def tokenize_into_words(self, sentence):
        tokens = word_tokenize(str(sentence).lower())
        tokens = [w for w in tokens if not w in self.stopwords]
        tokens = [w for w in tokens if not w in PUNCTUATION_SIGNS]
        return tokens

    def _calc_idf(self, documents):
        #print("calculating idf")
        bags_of_words = []

        for i, doc in enumerate(documents):
            doc_words = set()

            for sentence in doc:
                words = self.tokenize_into_words(sentence)
                doc_words.update(words)

            if doc_words:
                bags_of_words.append(doc_words)

        if not bags_of_words:
            raise ValueError('bag of words is empty')

        doc_number_total = len(bags_of_words)
        print("total docs processed %d" %doc_number_total)

        if self.include_new_words:
            default_value = 1

        else:
            default_value = 0

        idf_score = defaultdict(lambda: default_value)

        for word in set.union(*bags_of_words):
            doc_number_word = sum(1 for bag in bags_of_words if word in bag)
            idf_score[word] = math.log(doc_number_total / doc_number_word)
        #print("idf scores done")
        return idf_score

    def _calc_sim_matrix(self, tf_scores):
        length = len(tf_scores)

        matrix = np.zeros([length] * 2)

        for i in range(length):
            for j in range(i, length):
                similarity = self._idf_modified_cosine(tf_scores, i, j)

                if similarity:
                    matrix[i, j] = similarity
                    matrix[j, i] = similarity

        return matrix

    def _idf_modified_cosine(self, tf_scores, i, j):
        if i == j:
            return 1

        tf_i, tf_j = tf_scores[i], tf_scores[j]
        words_i, words_j = set(tf_i.keys()), set(tf_j.keys())

        nominator = 0

        for word in words_i & words_j:
            idf = self.idf_score[word]
            nominator += tf_i[word] * tf_j[word] * idf ** 2

        if math.isclose(nominator, 0):
            return 0

        denominator_i, denominator_j = 0, 0

        for word in words_i:
            tfidf = tf_i[word] * self.idf_score[word]
            denominator_i += tfidf ** 2

        for word in words_j:
            tfidf = tf_j[word] * self.idf_score[word]
            denominator_j += tfidf ** 2

        similarity = nominator / math.sqrt(denominator_i * denominator_j)

        return similarity

def create_markov_matrix(weights_matrix):
    n_1, n_2 = weights_matrix.shape
    if n_1 != n_2:
        raise ValueError('weights_matrix should be square')

    row_sum = weights_matrix.sum(axis=1, keepdims=True)

    return weights_matrix / row_sum


def create_markov_matrix_discrete(weights_matrix, threshold):
    discrete_weights_matrix = np.zeros(weights_matrix.shape)
    ixs = np.where(weights_matrix >= threshold)
    discrete_weights_matrix[ixs] = 1

    return create_markov_matrix(discrete_weights_matrix)

def _power_method(transition_matrix):
    eigenvector = np.ones(len(transition_matrix))

    if len(eigenvector) == 1:
        return eigenvector

    transition = transition_matrix.transpose()

    while True:
        eigenvector_next = np.dot(transition, eigenvector)

        if np.allclose(eigenvector_next, eigenvector):
            return eigenvector_next

        eigenvector = eigenvector_next
        #increases speed but also increases space taken
        transition = np.dot(transition, transition)

def degree_centrality_scores(sim_matrix, threshold=None):
    if not (threshold is None or isinstance(threshold, float) and 0 <= threshold < 1):
        raise ValueError('threshold should be a floating-point number ''from the interval [0, 1) or None')

    if threshold is None:
        markov_matrix = create_markov_matrix(sim_matrix)
    else:
        markov_matrix = create_markov_matrix_discrete(sim_matrix, threshold)
    scores = stationary_distribution(markov_matrix, normalized=False)
    return scores

def stationary_distribution(transition_matrix, normalized=True):
    n_1, n_2 = transition_matrix.shape
    if n_1 != n_2:
        raise ValueError('transition_matrix should be square')

    distribution = np.zeros(n_1)
    grouped_indices = connected_nodes(transition_matrix)

    for group in grouped_indices:
        t_matrix = transition_matrix[np.ix_(group, group)]
        eigenvector = _power_method(t_matrix)
        distribution[group] = eigenvector

    if normalized:
        distribution /= n_1

    return distribution

def connected_nodes(matrix):
    _, labels = connected_components(matrix)
    groups = []
    for tag in np.unique(labels):
        group = np.where(labels == tag)[0]
        groups.append(group)

    return groups
