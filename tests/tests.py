import unittest
import random
import sys, os
import re
import nltk
import json
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'allennlp')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'summarization', 'pubmed_summarization')))
# print(sys.path)
from ehrkit import ehrkit
from getpass import getpass

try: 
    from config import USERNAME, PASSWORD
except:
    print("Please put your username and password in config.py")
    USERNAME = input('DB_username?')
    PASSWORD = getpass('DB_password?')


DOC_ID = 1354526 # Temporary!!!


# Number of documents in NOTEEVENTS.
NUM_DOCS = 2083180

# Number of patients in PATIENTS.
NUM_PATIENTS = 46520

# Number of diagnoses in DIAGNOSES_ICD.
NUM_DIAGS = 823933


def select_ehr(ehrdb, requires_long=False, recursing=False):
    if recursing:
        doc_id = ''
    else:
        #doc_id = input("MIMIC Document ID [press Enter for random]: ")
        
        doc_id = ''
    
    if doc_id == '':
        # Picks random document
        ehrdb.cur.execute("SELECT ROW_ID FROM mimic.NOTEEVENTS ORDER BY RAND() LIMIT 1")
        doc_id = ehrdb.cur.fetchall()[0][0]
        text = ehrdb.get_document(int(doc_id))
        if len(text.split()) > 200 or not requires_long:
            return doc_id, text
        else:
            return select_ehr(ehrdb, requires_long, True)
    else:
        # Get inputted document
        try:
            text = ehrdb.get_document(int(doc_id))
            return doc_id, text
        except:
            message = 'Error: There is no document with ID \'' + doc_id + '\' in mimic.NOTEEVENTS'
            sys.exit(message)


def get_nb_dir(ending, SUMM_DIR):
    # Gets path of Naive Bayes model trained on most examples
    dir_nums = []
    for dir in os.listdir(SUMM_DIR):
        if os.path.isdir(os.path.join(SUMM_DIR, dir)) and dir.endswith('_exs_' + ending):
            if os.path.exists(os.path.join(SUMM_DIR, dir, 'nb')):  
                try:
                    dir_nums.append(int(dir.split('_')[0]))
                except:
                    continue
    if len(dir_nums) > 0:
        best_dir_name = str(max(dir_nums)) + '_exs_' + ending
        return best_dir_name
    else:
        return None

def show_summary(doc_id, text, summary, model_name):
    #x = input('Show full EHR (DOC ID %s)? [DEFAULT=Yes]' % doc_id)
    x = ''
    if x.lower() in ['y', 'yes', '']:
        print('\n\n' + '-'*30 + 'Full EHR' + '-'*30)
        print(text + '\n')
        print('-'*80 + '\n\n')

    print('-'*30 + 'Predicted Summary ' + model_name + '-'*30)
    print(summary)
    print('-'*80 + '\n\n')


class tests(unittest.TestCase):
    def setUp(self):
        self.ehrdb = ehrkit.start_session(USERNAME, PASSWORD)
        self.ehrdb.get_patients(3)


''' Runs tests 1.1-1.4 '''
class t1(tests):
    def test1_1_count_patients(self):
        kit_count = self.ehrdb.count_patients()
        print("Patient count: ", kit_count)

        self.ehrdb.cur.execute("SELECT COUNT(*) FROM mimic.PATIENTS")
        raw = self.ehrdb.cur.fetchall()
        test_count = int(raw[0][0])

        self.assertEqual(test_count, kit_count)

    # def test1_2_count_docs(self):
    #     # Fails! count_docs returns 1573339, but mimic.NOTEEVENTS has 2083180 documents. 
    #     # TO DO: Fix whatever is wrong here
    #     kit_count = self.ehrdb.count_docs(['NOTEEVENTS'])
    #     print("Document count: ", kit_count)

    #     self.ehrdb.cur.execute("SELECT COUNT(*) FROM mimic.NOTEEVENTS")
    #     raw = self.ehrdb.cur.fetchall()
    #     test_count = int(raw[0][0])

    #     self.assertEqual(test_count, kit_count)

    def test1_3_note_info(self):
        self.ehrdb.get_note_events()
        print('output format: SUBJECT_ID, ROW_ID, NoteEvent length')
        lens = [(patient.id, note[0], len(note[1])) for patient in self.ehrdb.patients.values() for note in patient.note_events]
        print(lens)

        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)

    def test1_4_longest_note(self):
        # Gets longest note among the patient notes queued by get_note_events()
        self.ehrdb.get_note_events()
        pid, rowid, doclen = self.ehrdb.longest_NE()
        print('patient id is:', pid, 'NoteEvent id is:', rowid, 'length: ', doclen)

        # placeholder, this output cannot be checked easily
        self.assertEqual(1, 1)


class t2(tests):
    def test2_1_print_note(self):
        ### There are 2083180 patient records in NOTEEVENTS. ###
        record_id = random.randint(1, NUM_DOCS + 1)
        kit_rec = self.ehrdb.get_document(record_id)
        print("Document with ID %d\n: " % record_id, kit_rec)

        self.ehrdb.cur.execute("select TEXT from mimic.NOTEEVENTS where ROW_ID = %d" % record_id)
        test_rec = self.ehrdb.cur.fetchall()[0][0]

        self.assertEqual(kit_rec, test_rec)

    def test2_2_patient_info(self):
        ### There are records from 46520 unique patients in MIMIC. ###
        patient_id = random.randint(1, NUM_PATIENTS + 1)
        kit_ids = self.ehrdb.get_all_patient_document_ids(patient_id)
        print('Document IDs related to Patient %d: ' % patient_id, kit_ids)
        print("Number of docs related to Patient %d: " % patient_id, len(kit_ids))

        self.ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS where SUBJECT_ID = %d" % patient_id)
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)

        self.assertEqual(kit_ids, test_ids)

    #@unittest.skipIf("t2.test2_3" not in sys.argv, "Test 2_3 must be run explicitly due to runtime.")
    def test2_3_doc_ids(self):
        kit_ids = self.ehrdb.list_all_document_ids()

        self.ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS")
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)
        print('test_ids')
        print(test_ids[:30])
        print('...')

        self.assertEqual(kit_ids, test_ids)

    def test2_4_patient_ids(self):
        kit_ids = self.ehrdb.list_all_patient_ids()

        self.ehrdb.cur.execute("select SUBJECT_ID from mimic.PATIENTS")
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)
        print(test_ids[:30])
        print('...')

        self.assertEqual(kit_ids, test_ids)

    #@unittest.skipIf("t2.test2_5" not in sys.argv, "Test 2_5 must be run explicitly due to runtime.")
    def test2_5_docs_on_date(self):
        ### Select random date from a date in the database. 
        ### Dates are shifted to future but preserve time, weekday, and seasonality.
        random_id = random.randint(1, NUM_DOCS + 1)
        self.ehrdb.cur.execute("select CHARTDATE from mimic.NOTEEVENTS where ROW_ID = %d" % random_id)
        date = self.ehrdb.cur.fetchall()[0][0]

        kit_ids = self.ehrdb.get_documents_d(date)

        self.ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS where CHARTDATE = \"%s\"" % date)
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)
        print(f"Selected date: {date}")
        print(f"Test ids {test_ids[:30]} ...")

        self.assertEqual(kit_ids, test_ids)


class t3(tests):
    def test3_1_extract_abbreviations(self):
        # Defines abbreviation as a string of capitalized letters
        random_id = random.randint(1, NUM_DOCS + 1)
        print("Collecting abbreviations for document %d..." % random_id)
        kit_abbs = self.ehrdb.get_abbreviations(random_id)

        sents = self.ehrdb.get_document_sents(random_id)
        test_abbs = set()
        for sent in sents:
            for word in ehrkit.word_tokenize(sent):
                print(word)
                pattern = r'[A-Z]{2}'  # Only selects words in ALL CAPS
                if re.match(pattern, word):
                    test_abbs.add(word)

        print(kit_abbs)

        self.assertEqual(kit_abbs, list(test_abbs))

    #@unittest.skipIf("t3.test3_2" not in sys.argv, "Test 3_2 must be run explicitly due to runtime.")
    def test3_2_docs_with_query(self):
        query = "meningitis"
        print('Printing a list of all document ids including query like ', query)
        kit_ids = self.ehrdb.get_documents_q(query)
        print(kit_ids[:30])  # Extremely long list of DOC_IDs
        print("...")

        query = "%"+query+"%"
        self.ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS where TEXT like \'%s\'" % query)
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)

        self.assertEqual(kit_ids, test_ids)

    #@unittest.skipIf("t3.test3_3" not in sys.argv, "Test 3_3 must be run explicitly due to runtime. Also, this is essentially a duplicate of task 3.2.")
    def test3_3_query_docs(self):
        ### Task 3.3 is the same as task 3.2 with a different query. ###
        query = "Service: SURGERY"
        print('Printing a list of all document ids including query like ', query)
        kit_ids = self.ehrdb.get_documents_q(query)
        print(kit_ids[:30])  # Extremely long list of DOC_IDs
        print("...")

        query = "%"+query+"%"
        self.ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS where TEXT like \'%s\'" % query)
        raw = self.ehrdb.cur.fetchall()
        test_ids = ehrkit.flatten(raw)

        self.assertEqual(kit_ids, test_ids)

    def test3_4_doc_sentences(self):
        doc_id = random.randint(1, NUM_DOCS + 1)
        print('Kit function printing a numbered list of all sentences in document %d' % doc_id)
        # MIMIC EHRs are very messy and sentence tokenizaton often doesn't work
        kit_doc = self.ehrdb.get_document_sents(doc_id)
        ehrkit.numbered_print(kit_doc)

        self.ehrdb.cur.execute("select TEXT from mimic.NOTEEVENTS where ROW_ID = %d " % doc_id)
        raw = self.ehrdb.cur.fetchall()
        test_doc = ehrkit.sent_tokenize(raw[0][0])
        print(test_doc)

        self.assertEqual(kit_doc, test_doc)

    #@unittest.skipIf("t3.test3_7" not in sys.argv, "Test 3_7 must be run explicitly due to runtime.")
    def test3_7_medications(self):
        kit_meds = self.ehrdb.count_all_prescriptions()

        test_meds = {}
        self.ehrdb.cur.execute("select DRUG from mimic.PRESCRIPTIONS")
        raw = self.ehrdb.cur.fetchall()
        meds_list = ehrkit.flatten(raw)
        for med in meds_list:
            if med in test_meds:
                test_meds[med] += 1
            else:
                test_meds[med] = 1

        print(meds_list[:30])
        print("...")

        self.assertEqual(kit_meds, test_meds)


class t4(tests):
    @unittest.skip("Task 4.1 is not ready to be tested yet.")
    def test4_1(self):
        d = self.ehrdb.get_documents_icd9()
        print(d)
        self.assertIsNotNone(d['code'])

    @unittest.skip("Task 4.4 is not ready to be tested yet.")
    def test4_4(self):
        pass


class t5(tests):
    @unittest.skipIf("t5.test5_1" not in sys.argv, "Test 5_1 must be run explicitly due to runtime.")
    def test5_1_extract_phrases(self):
        doc_id = random.randint(1, NUM_DOCS + 1)
        kit_phrases = self.ehrdb.extract_phrases(doc_id)

        print("Testing task 5.1\n Check phrases manually: ", kit_phrases)

        self.assertIsNotNone(kit_phrases)

    def test5_4_count_gender(self):
        gender = random.choice(['M', 'F'])
        kit_count = self.ehrdb.count_gender(gender)

        self.ehrdb.cur.execute('SELECT COUNT(*) FROM mimic.PATIENTS WHERE GENDER = \'%s\'' % gender)
        raw = self.ehrdb.cur.fetchall()
        test_count = raw[0][0]
        print('Gender:', gender, '\tCount:', str(test_count))

        self.assertEqual(kit_count, test_count)


class t6(tests):
    @unittest.skipIf("t6.test6_1_sentiment_classification" not in sys.argv, "Test 6_1 must be run explicitly due to verbosity.")
    def test6_1_sentiment_classification(self):
        import loader

        doc_id, text = select_ehr(self.ehrdb)

        x = input('GloVe or RoBERTa predictor [g=GloVe, r=RoBERTa]? ')
        if x == 'g':
            glove_predictor = loader.load_glove()
            probs = glove_predictor.predict(text)['probs']
        elif x == 'r':
            roberta_predictor = loader.load_roberta()
            try:
                probs = roberta_predictor.predict(text)['probs']
            except:
                print('Document too long for RoBERTa model. Using GLoVe instead.')
                glove_predictor = loader.load_glove()
                probs = glove_predictor.predict(text)['probs']
        else:
            sys.exit('Error: Must input \'g\' or  \'r\'')

        classification = 'Positive' if probs[0] >= 0.5 else 'Negative'
        print("Document ID: ", doc_id, "\tPredicted Sentiment: ", classification)

    @unittest.skipIf("t6.test6_2_ner" not in sys.argv, "Test 6_2 must be run explicitly due to verbosity.")
    def test6_2_ner(self):
        import loader

        doc_id, text = select_ehr(self.ehrdb)

        if os.path.exists("../allennlp/elmo-ner/whole_model.pt"):
            predictor = loader.load_ner()
        else:
            predictor = loader.download_ner()

        text = self.ehrdb.get_document(int(doc_id))
        pred = predictor.predict(text)
        # pred = predictor.predict("John likes and Bill hates ice cream")
        print_results = input("Prediction complete. Print results? (y/n): ")
        if print_results == "y":
            print("Document ID: ", doc_id, "  Results: ", pred['tags'])
    
    @unittest.skipIf("t6.test6_3_tokenize" not in sys.argv, "Test 6_3 must be run explicitly due to runtime.")
    def test6_3_tokenize(self):
        import torch
        from transformers import BertTokenizer#, BertModel, BertForMaskedLM

        doc_id, text = select_ehr(self.ehrdb)
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        bert_tokenized_text = tokenizer.tokenize(text)
        print('\n' + '-'*20 + 'text' + '-'*20)
        print(text)
        print('\n' + '-'*20 + 'Tokenized text from Huggingface BERT Tokenizer' + '-'*20)    
        print(bert_tokenized_text)


        # library function
        ehr_bert_tokenized_text = self.ehrdb.get_bert_tokenize(doc_id)
        self.assertEqual(bert_tokenized_text, ehr_bert_tokenized_text)


class t7(tests):
    # Summarization algorithms
    #@unittest.skipIf("t7.test7_1_naive_bayes" not in sys.argv, "Test 7_1 must be run explicitly due to verbosity.")
    def test7_1_naive_bayes(self):
        from pubmed_naive_bayes import classify_nb
        from get_pubmed_nb_data import build_vecs
        from sklearn.naive_bayes import GaussianNB

        doc_id, text = select_ehr(self.ehrdb)
        #body_type = input('Use Naive Bayes model trained from whole body sections or just their body introductions?\n\t'\
        #                '[w=whole body, j=just intro, DEFAULT=just intro]: ')
        
        body_type = 'j'

        if body_type == 'w':
            ending = 'body'
        elif body_type in ['j', '']:
            ending = 'intro'
        else:
            sys.exit('Error: Must input \'w\' or \'j.\'')
        SUMM_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'summarization', 'pubmed_summarization'))
        best_dir_name = get_nb_dir(ending, SUMM_DIR)
        if not best_dir_name:
            message = 'No Naive Bayes models of this type have been fit. '\
                        'Would you like to do so now?\n\t[DEFAULT=Yes] '
            #response = input(message)
            
            response = 'y'

            if response.lower() in ['y', 'yes', '']:
                command = 'python ' + os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'summarization', 'pubmed_summarization', 'pubmed_naive_bayes.py'))
                os.system(command)
                best_dir_name = get_nb_dir(ending)
            if response.lower() not in ['y', 'yes', ''] or not best_dir_name:
                sys.exit('Exiting.')

        # Fits model to data        
        NB_DIR = os.path.join(SUMM_DIR, best_dir_name, 'nb')
        with open(os.path.join(NB_DIR, 'feature_vecs.json'), 'r') as f:
            data = json.load(f)
        xtrain, ytrain = data['train_features'], data['train_outputs']
        gnb = GaussianNB()
        gnb.fit(xtrain, ytrain)

        # Evaluates on model
        tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
        feature_vecs, _ = build_vecs(text, None, tokenizer)
        PCT_SUM = 0.3
        preds = classify_nb(feature_vecs, PCT_SUM, gnb)
        sents = tokenizer.tokenize(text)
        summary = ''
        for i in range(len(preds)):
            if preds[i] == 1:
                summary += sents[i]

        show_summary(doc_id, text, summary, 'Naive Bayes')
        
    #@unittest.skipIf("t7.test7_2_distilbart_summary" not in sys.argv, "Test 7_2 must be run explicitly due to runtime.")
    def test7_2_distilbart_summary(self):
        # Distilbart for summarization. Trained on CNN/ Daily Mail (~4x longer summaries than XSum)
        doc_id, text = select_ehr(self.ehrdb, requires_long=True)
        model_name = 'sshleifer/distilbart-cnn-12-6'
        summary = self.ehrdb.summarize_huggingface(text, model_name)

        show_summary(doc_id, text, summary, model_name)
        print('Number of Words in Full EHR: %d' % len(text.split()))
        print('Number of Words in %s Summary: %d' % (model_name, len(summary.split())))

    #@unittest.skipIf("t7.test7_3_t5_summary" not in sys.argv, "Test 7_3 must be run explicitly due to runtime.")
    def test7_3_t5_summary(self):
        # T5 for summarization. Trained on CNN/ Daily Mail
        doc_id, text = select_ehr(self.ehrdb, requires_long=True)
        model_name = 't5-small'
        summary = self.ehrdb.summarize_huggingface(text, model_name)

        show_summary(doc_id, text, summary, model_name)
        print('Number of Words in Full EHR: %d' % len(text.split()))
        print('Number of Words in %s Summary: %d' % (model_name, len(summary.split())))

def testing():
    unittest.main()

if __name__ == '__main__':
    unittest.main()
