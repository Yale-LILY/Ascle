import unittest
import random
import sys, os
import glob
import itertools
import shutil
from pathlib import Path
from nltk import sent_tokenize

#from ehrkit.summarizers import Lexrank
#from ehrkit.summarizers.evaluate import folder2rouge

from summarizers import Lexrank
from summarizers.evaluate import folder2rouge

import files2rouge

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Number of documents used
NUM_DOCS = 20

class tests(unittest.TestCase):
    def setUp(self):
        self.source_dir = '/data/lily/jmg277/nc_text/source'
        self.source_dir_body = '/data/lily/jmg277/nc_text_body/source'
        self.target_dir = '/data/lily/jmg277/nc_text/target'

class t1(tests):
    def test1_1(self):
        print("test 1.1 Avg sentences in introduction source")
        sentence_counts = []
        for filepath in glob.glob(os.path.join(self.source_dir, '*.src')):
            with open(filepath) as fp:
                num_sentences = 0 
                for line in fp.readlines():
                    num_sentences += len(sent_tokenize(line))
                sentence_counts.append(num_sentences)
        avg = round(sum(sentence_counts)/len(sentence_counts))
        print("Mean number of sentences in source (introduction section) text:", avg)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

    def test1_2(self):
        print("test 1.2 Avg sentences in entire body source")
        sentence_counts = []
        for filepath in glob.glob(os.path.join(self.source_dir_body, '*.src')):
            with open(filepath) as fp:
                num_sentences = 0 
                for line in fp.readlines():
                    num_sentences += len(sent_tokenize(line))
                sentence_counts.append(num_sentences)
        avg = round(sum(sentence_counts)/len(sentence_counts))
        print("Mean number of sentences in source (entire body) text:", avg)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

    def test1_3(self):
        print("test 1.3 Avg sentences in abstracts")
        sentence_counts = []
        for filepath in glob.glob(os.path.join(self.target_dir, '*.tgt')):
            with open(filepath) as fp:
                num_sentences = 0 
                for line in fp.readlines():
                    num_sentences += len(sent_tokenize(line))
                sentence_counts.append(num_sentences)
        avg = round(sum(sentence_counts)/len(sentence_counts))
        print("Mean number of sentences in abstract text:", avg)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

class t2(tests):
    def setUp(self):
        self.source_dir = '/data/lily/jmg277/nc_text/source'
        self.target_dir = '/data/lily/jmg277/nc_text/target'
        self.source_dir_body = '/data/lily/jmg277/nc_text_body/source'
        self.target_dir_body = '/data/lily/jmg277/nc_text_body/target'
        self.saveto_dir = '/data/lily/sn482/pubmed_summaries'
       
        documents = {} 
        if not os.path.exists(self.saveto_dir):
            os.mkdir(self.saveto_dir)

        for i, filepath in enumerate(glob.glob(os.path.join(self.source_dir, '*.src'))):
            with open(filepath) as fp:
                fname = Path(filepath).stem
                sentences = [] 
                for line in fp.readlines():
                    sentences.extend(sent_tokenize(line))
                documents[fname] = sentences
            if i == NUM_DOCS - 1:
                break
        self.documents = documents

    def test2_1(self):
        print("test 2.1 idf scores")
        num_testdocs = 3

        test_docs = dict(itertools.islice(self.documents.items(), num_testdocs))
        lxr = Lexrank(test_docs.values(), threshold=.1)
        print(lxr.idf_score)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

    def test2_2(self):
        print("test 2.2 intro lexrank summaries trained on intro text")
        new_dir = "lexrank_summaries"
        new_dir_path = os.path.join(self.saveto_dir, new_dir)
        if os.path.exists(new_dir_path):
            shutil.rmtree(new_dir_path)
        os.mkdir(new_dir_path)

        lxr = Lexrank(self.documents.values(), threshold=.1)
        test_docs = self.documents
        #dict(itertools.islice(self.documents.items(), 3)) #documents[:3]
        for fname in test_docs:
            summary = lxr.get_summary(test_docs[fname], summary_size=10)#, threshold=.1)
            joined_summary = " ".join(summary)
            summary_path = os.path.join(new_dir_path, fname + ".sum")
            with open(summary_path, 'w') as sum:
                sum.write(joined_summary)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

class t3(tests):
    def setUp(self):
        self.ref_dir = '/data/lily/sn482/reference_abstracts'
        self.lxrsummaries_dir = '/data/lily/sn482/pubmed_summaries/lexrank_summaries'

    def test3_1(self):
        print("test 3.1 files2rouge lexrank summaries")
        
        allsummaries_path = os.path.join(self.lxrsummaries_dir, 'allsummaries.txt')
        allreferences_path = os.path.join(self.lxrsummaries_dir, 'allreferences.txt')
        #saveto_path = os.path.join(self.saveto_path, "lexrank_rouge.txt")

        allsummaries_file = open(allsummaries_path, 'w')
        allreferences_file = open(allreferences_path, 'w')

        for filepath in glob.glob(os.path.join(self.lxrsummaries_dir, '*.sum')):
            fname = Path(filepath).stem
            
            with open(filepath) as fs:
                summary = fs.readline()
                allsummaries_file.write("%s\n" % summary)

            ref_path = os.path.join(self.ref_dir, fname + ".tgt")

            with open(ref_path) as fr:
                abstract = fr.readline()
                allreferences_file.write("%s\n" % abstract)

        allsummaries_file.close()
        allreferences_file.close()

        files2rouge.run(allsummaries_path, allreferences_path)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

    def test3_2(self):
        print("test 3.2 folder2rouge lexrank summaries")
        # saveto_path = os.path.join(self.saveto_dir, "lxr_folder2rouge.txt")
        rouge = folder2rouge(self.lxrsummaries_dir, self.ref_dir)
        rouge.run()#saveto=saveto_path)
        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

if __name__ == '__main__':
    unittest.main()
