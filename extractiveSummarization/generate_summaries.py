import sys, os
import glob
import itertools
import shutil
import time
from pathlib import Path
from nltk import sent_tokenize
from summarizers import Lexrank

import argparse
parser = argparse.ArgumentParser()

parser.add_argument('--train', action='store', metavar='path', type=str, required=True,  help='Directory path containing training documents. If test path not specified, also treated as testing documents.')
parser.add_argument('--saveto', action='store', metavar='path', type=str, required=True, help='directory path for saving summaries produced')
parser.add_argument('--test', action='store', metavar='path', type=str, help='directory path containing testing documents')
parser.add_argument('--ntrain', action='store', type=int, metavar='n', help='First n number of documents to train on')
parser.add_argument('--ntest', action='store', type=int, metavar='n', help='First n number of documents to produce summaries for')
parser.add_argument('--threshold', action='store', type=float, help="default 0.03")
parser.add_argument('--size', action='store', type=int, help='summary size. default 1')

args = parser.parse_args()

train_dir_path = args.train
test_dir_path = args.test
saveto_dir_path = args.saveto
threshold = args.threshold or 0.03
summary_size = args.size or 1

if not os.path.isdir(train_dir_path):
    print('The train path specified does not exist')
    sys.exit()

if test_dir_path and not os.path.isdir(test_dir_path):
    print('The test path specified does not exist')
    sys.exit()

if not os.path.isdir(saveto_dir_path):
    print('The save to path specified does not exist')
    sys.exit()

if args.ntest and args.ntest < 1:
    print('ntest should be greater than 0')

if args.ntrain and args.ntrain < 1:
    print('ntrain should be greater than 0')

start = time.time()

train_documents = {}
test_documents = {}

for i, filepath in enumerate(glob.glob(os.path.join(train_dir_path, '*'))):
    with open(filepath) as fp:
        fname = Path(filepath).stem
        sentences = [] 
        for line in fp.readlines():
            sentences.extend(sent_tokenize(line))
        train_documents[fname] = sentences
        if args.ntrain and i == args.ntrain - 1:
            break

if test_dir_path:
    for i, filepath in enumerate(glob.glob(os.path.join(test_dir_path, '*'))):
        with open(filepath) as fp:
            fname = Path(filepath).stem
            sentences = [] 
            for line in fp.readlines():
                sentences.extend(sent_tokenize(line))
            test_documents[fname] = sentences
        if args.ntest and i == args.ntest - 1:
            break

lxr = Lexrank(train_documents.values(), threshold=threshold)

if test_dir_path:
    documents = test_documents
else:
    documents = train_documents

for i, fname in enumerate(documents):
    summary = lxr.get_summary(documents[fname], summary_size=summary_size)#, threshold=.1)
    joined_summary = " ".join(summary)
    summary_path = os.path.join(saveto_dir_path, fname + ".sum")
    with open(summary_path, 'w') as sum:
        sum.write(joined_summary)
    if args.ntest and i == args.ntest - 1:
        break

end = time.time()
#print("----Summary----")
print("Runtime " + str(end - start))
