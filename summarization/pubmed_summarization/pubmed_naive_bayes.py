# Functions for extracting features from text
# Mostly taken from https://github.com/rachitjain2706/Auto-Text-sumarizer
import os
import sys
import shutil
import random
import json
from get_pubmed_nb_data import *
from sklearn.naive_bayes import GaussianNB
from sklearn import metrics
import nltk
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'rouge_git')))
from rouge import FilesRouge, Rouge


def choose_pubmed_files(PARSED_DIR, EXS_DIR, n_train):
    # 80/20 training/test split
    n_test = int(round(n_train / 4))
    abs_names = os.listdir(os.path.join(PARSED_DIR, 'abstract'))
    n_total = n_train + n_test
    if len(abs_names) < n_total:
        message = 'Error: Desired number of training + test examples is ' + str(n_total)
        message += '; however, only ' + str(len(abs_names)) + ' files parsed this way currently exist.'
        sys.exit(message)

    # Select examples
    random.shuffle(abs_names)
    training_file_names = [name[:-4] for name in abs_names][:n_train]
    test_file_names = [name[:-4] for name in abs_names][n_train:n_train+n_test]

    # Write to file
    with open(os.path.join(EXS_DIR, 'training_files.txt'), 'w') as train:
        train.writelines('%s\n' % name for name in training_file_names)
    with open(os.path.join(EXS_DIR, 'test_files.txt'), 'w') as test:
        test.writelines('%s\n' % name for name in test_file_names)


def classify_nb(x, pct_sum, gnb):
    # Runs through Gaussian Naive Bayes models
    if len(x) == 0:
        return [0]
    probs = gnb.predict_proba(x)

    # Classifies likeliest sentences as part of summary
    p_summary = [p[1] for p in probs]
    n_summary_sents = round(len(x)*pct_sum)
    if n_summary_sents == 0:
        n_summary_sents = 1
    thresh = sorted(p_summary)[len(x) - n_summary_sents]
    preds = [1 if i >= thresh else 0 for i in p_summary]
    return preds


def pubmed_naive_bayes(body_type=None, n_train=None):
    if not body_type:
        body_type = input('Train with articles\' whole body sections or just their body introductions?\n\t'
                      '[w=whole body, j=just intro, DEFAULT=just intro]: ')

    PARSED_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'pubmed', 'parsed_articles'))
    if not os.path.exists(PARSED_DIR):
        missing_path = 'Error: Directory of parsed files ' + PARSED_DIR + ' does not exist.'
        sys.exit(missing_path)
    if body_type.lower() == 'w':
        PARSED_DIR = os.path.join(PARSED_DIR, 'with_whole_bodies')
        whole_body = True
    elif body_type.lower() in ['j', '']:
        PARSED_DIR = os.path.join(PARSED_DIR, 'with_just_intros')
        whole_body = False
    else:
        sys.exit('Error: Must input \'w\' or \'j.\'')

    if not n_train:
        n_train = int(input('Number of examples for training set: '))

    exs_dir_name = str(n_train) + '_exs_body' if whole_body else str(n_train) + '_exs_intro'
    FILE_DIR = os.path.abspath(os.path.dirname(__file__))
    EXS_DIR = os.path.join(FILE_DIR, exs_dir_name)
    NB_DIR = os.path.join(EXS_DIR, 'nb')
    if not os.path.exists(NB_DIR):
        if n_train >= 1000 and not whole_body:
            verbose = True
        elif n_train >= 200 and whole_body:
            verbose = True
        else:
            verbose = False

        if verbose:
            message = 'To fit a Naive Bayes model on ' + str(n_train) + \
                ' training articles, feature vectors must be created from the data.' \
                'This can take a long time when the number of files is large. Do you wish to proceed? [Default=Yes]'
            x = input(message)
            proceed = 'y'
            if proceed.lower() not in ['', 'y', 'yes']:
                sys.exit('Exiting.')

        if not os.path.exists(os.path.join(EXS_DIR, 'training_files.txt')) \
                or not os.path.exists(os.path.join(EXS_DIR, 'test_files.txt')):
            # Selects and writes training and test files
            if not os.path.exists(EXS_DIR):
                os.mkdir(EXS_DIR)
            choose_pubmed_files(PARSED_DIR, EXS_DIR, n_train)

        # Creates feature and output vectors for Pubmed articles
        # get_pubmed_nb_data(PARSED_DIR, NB_DIR, n_train, whole_body, verbose)
        get_pubmed_nb_data(PARSED_DIR, NB_DIR, n_train, whole_body)

    # Loads training data
    with open(os.path.join(NB_DIR, 'feature_vecs.json'), 'r') as f:
        data = json.load(f)
    xtrain, ytrain = data['train_features'], data['train_outputs']

    # Fits model to data
    gnb = GaussianNB()
    gnb.fit(xtrain, ytrain)

    # Calculates training accuracy
    pct_sum = sum(ytrain) / len(ytrain)
    p_guess_correct = (1-pct_sum)**2 + pct_sum**2
    print('\nTraining Accuracy of Random Guessing: {}%'.format(round(p_guess_correct*100, 1)))
    train_preds = classify_nb(xtrain, pct_sum, gnb)
    print('Training Accuracy of Model: {}%'
          .format(round(metrics.accuracy_score(ytrain, train_preds)*100), 1))

    # Calculates average test accuracy
    ytest = data['test_outputs']
    pct_sum = sum(ytest) / len(ytest)
    p_guess_correct = (1-pct_sum)**2 + pct_sum**2
    print('\nTest Accuracy of Random Guessing: {}%'.format(round(p_guess_correct * 100, 1)))
    
    test_accuracies = []
    os.makedirs(os.path.join(NB_DIR, 'test_summary'), exist_ok=True)
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    for file in os.listdir(os.path.join(NB_DIR, 'test_json')):
        # Classifies sentences in each test file
        with open(os.path.join(NB_DIR, 'test_json', file), 'r') as f:
            test_data = json.load(f)
        xtest, ytest = test_data['features'], test_data['outputs']
        pct_sum = sum(ytest) / len(ytest)
        test_preds = classify_nb(xtest, pct_sum, gnb)
        test_accuracies.append(metrics.accuracy_score(ytest, test_preds))

        summary_path = os.path.join(NB_DIR, 'test_summary', file[:-5] + '.sum')
        if not os.path.exists(summary_path):
            # Gets text corresponding to summary classifications
            with open(os.path.join(PARSED_DIR, 'merged', file[:-5] + '.mgd'), 'r') as mgd:
                mgd_text = mgd.read().replace('\n', '. ').replace('..', '.')
            mgd_sents = tokenizer.tokenize(mgd_text)
            summary = ''
            for i in range(len(test_preds)):
                if test_preds[i] == 1:
                    summary += mgd_sents[i]

            # Writes to file
            with open(summary_path, 'w') as s:
                s.write(summary + '\n')

    avg_pct_acc = round((sum(test_accuracies) / len(test_accuracies)*100), 1)
    print('Model Average Test Accuracy: {}%'.format(avg_pct_acc))

    rouge_path = os.path.join(NB_DIR, 'ROUGE.txt')
    if not os.path.exists(rouge_path):
        # Initialize ROUGE class
        rouge_scores = {'rouge-1': {'f': 0.0, 'p': 0.0, 'r': 0.0},
                        'rouge-2': {'f': 0.0, 'p': 0.0, 'r': 0.0},
                        'rouge-l': {'f': 0.0, 'p': 0.0, 'r': 0.0}}
        rouge_scores_random = {'rouge-1': {'f': 0.0, 'p': 0.0, 'r': 0.0},
                               'rouge-2': {'f': 0.0, 'p': 0.0, 'r': 0.0},
                               'rouge-l': {'f': 0.0, 'p': 0.0, 'r': 0.0}}
        sum_files = os.listdir(os.path.join(NB_DIR, 'test_summary'))
        files_rouge = FilesRouge()
        for sum_file in sum_files:
            sum_path = os.path.join(NB_DIR, 'test_summary', sum_file)
            tgt_path = os.path.join(PARSED_DIR, 'abstract', sum_file[:-4] + '.tgt')
            rand_sum_path = os.path.join(PARSED_DIR, 'random_summary', sum_file[:-4] + '.sum')
            # Calculates ROUGE score of predicted and random summaries
            scores = files_rouge.get_scores(sum_path, tgt_path, avg=True)
            random_scores = files_rouge.get_scores(rand_sum_path, tgt_path, avg=True) # Compares against random summary of same size
            for i in rouge_scores.keys():
                for j in rouge_scores['rouge-1'].keys():
                    rouge_scores[i][j] += scores[i][j]
                    rouge_scores_random[i][j] += random_scores[i][j] 

        # Calculates average ROUGE scores
        for i in rouge_scores.keys():
            for j in rouge_scores['rouge-1'].keys():
                rouge_scores[i][j] /= len(sum_files)
                rouge_scores_random[i][j] /= len(sum_files)

        with open(rouge_path, 'w+') as scores:
            scores.write('\t' * 4)
            scores.write('Model')
            scores.write('\t' * 2)
            scores.write('Random Guessing\n')
            for i in range(1, 4):
                rouge_text = 'ROUGE-' + str(i) + ' Average ' if i < 3 else 'ROUGE-L Average '
                rouge_key = 'rouge-' + str(i) if i < 3 else 'rouge-l'
                scores.write(rouge_text + 'Precision:\t' + str(round(rouge_scores[rouge_key]['p'], 3)) + '\t\t')
                scores.write(str(round(rouge_scores_random[rouge_key]['p'], 3)) + '\n')
                scores.write(rouge_text + 'Recall:\t\t' + str(round(rouge_scores[rouge_key]['r'], 3)) + '\t\t')
                scores.write(str(round(rouge_scores_random[rouge_key]['r'], 3)) + '\n')
                scores.write(rouge_text + 'F1 Score:\t' + str(round(rouge_scores[rouge_key]['f'], 3)) + '\t\t')
                scores.write(str(round(rouge_scores_random[rouge_key]['f'], 3)) + '\n')
                if i < 3:
                    scores.write('-'*20 + '\n')
            scores.seek(0)
            print('\n' + scores.read())
    else:
        with open(rouge_path, 'r') as scores:
            print('\n' + scores.read())

    if os.path.exists('__pycache__'):
        shutil.rmtree('__pycache__')


if __name__ == '__main__':
    sys.setrecursionlimit(3000)
    pubmed_naive_bayes()
