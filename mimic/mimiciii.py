from datetime import date
import pymysql
#from sshtunnel import SSHTunnelForwarder
from classes import Patient, Disease, Diagnosis, Prescription, Procedure
from solr_lib import *
from datetime import datetime
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from gensim import corpora, models, similarities
from collections import defaultdict
import re
import sys
import os
import pprint
import string
import torch
import requests
from sklearn.feature_extraction.text import TfidfVectorizer

dir_path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
sys.path.append(dir_path)
# from scripts.train_word2vec import train_word2vec
# from scripts.abb_extraction import output_abb


# TODO: adding external library
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

class ehr_db:
    """Connection object to Tangra MySQL Server.

    Attributes:
        cnx: pymysql connection object
        cur: pymysql cursor object
    """

    def __init__(self, sess):
        self.cnx = sess['cnx']
        self.cur = sess['cur']
        self.patients = {}
        self.note_event_flag = False


    def get_patients(self, n):
        """Retrieves n patient objects from the database, adds them to self.patients

        Note:
            Patient sorted by ROW_ID in database
        Note:
            If n == -1, returns all patients.
        Args:
            n (int): Number of patient objects to return
        Returns:
            none
        """
        if n == -1:
            self.cur.execute("SELECT SUBJECT_ID, GENDER, DOB, DOD FROM mimic.PATIENTS")
        else:
            self.cur.execute("SELECT SUBJECT_ID, GENDER, DOB, DOD FROM mimic.PATIENTS LIMIT %d" % n)
        raw = self.cur.fetchall()


        for p in raw:
            data = {}
            data["id"] = p[0]
            data["sex"] = p[1]
            data["dob"] = p[2]

            # QUESTION: why use %Y and not %y? %Y only holds last two digits of year. How to tell difference between 100yo patient and newborn?
            if data["dob"] != None and isinstance(data["dob"], str):
                data["dob"] = datetime.strptime(data["dob"][0:10], "%Y-%m-%d")

            data["dod"] = p[3]

            # if data["dod"] != None and isinstance(data["dod"], str):
            #     import pdb;pdb.set_trace()
            #     data["dod"] = datetime.strptime(data["dod"][0:10], "%Y-%m-%d")


            data["alive"] = (data["dod"] == None)

            self.patients[data["id"]] = Patient(data)


    def count_patients(self):
        '''Counts and returns the number of patients as an int in the database.'''

        self.cur.execute("SELECT COUNT(*) FROM mimic.PATIENTS")
        raw = self.cur.fetchall()
        return int(raw[0][0])

    def count_docs(self, query, getAll = False, inverted = False):
        '''
        returns document count of tables
        query is a list of table names
        setting getAll to true returns count of all rows in all tables
        setting inverted = False returns count of rows in tables specified in *args
        setting inverted = True returns count of rows in all tables except those specified in *args
        '''
        table_count = self.cur.execute("SELECT TABLE_NAME, TABLE_ROWS from information_schema.tables where TABLE_SCHEMA = 'mimic' ")
        numtup = self.cur.fetchall()
        #numtup(nested tuple) structure: ((TABLE_NAME(str), TABLE_ROWS(int)),...)
        count = 0
        if getAll:
            for i in range(table_count):
                count = count + numtup[i][1]
            return count
        if inverted:
            for i in range(table_count):
                if numtup[i][0] in query:
                    continue
                count = count+numtup[i][1]
            return count
        for i in range(table_count):
            if numtup[i][0] in query:
                count = count+numtup[i][1]
        return count


    #is this redundant?

    def get_note_events(self):
        """
        adds note_events to patient objects in self.patients
        depends on get_patients(have to call it first to populate ehrdb with patients)
        return: None
        """
        #TODO: Currently only adds one NoteEvent
        for patient in self.patients.values():
            if patient.note_events is None:
                self.cur.execute("select ROW_ID, TEXT from mimic.NOTEEVENTS where SUBJECT_ID = %d" %patient.id)
                rawt = self.cur.fetchall()
                ls = []
                for p in rawt:
                    sent_list = sent_tokenize(p[1])
                    ls.append((p[0],sent_list))
                    patient.addNE(ls)
        self.note_event_flag = True

    def longest_NE(self):
        '''
        returns the longest note event in the patient dict
        '''
        #TODO: Currently only considers one NoteEvent per patient
        maxpid, maxlen = None, 0
        for patient in self.patients.values():
            for doc in patient.note_events:
                pid = patient.id
                rowid = doc[0]
                leng = len(doc[1])
                if leng>maxlen:
                    maxlen = leng
                    maxpid = pid
                    maxrowid = rowid
        return maxpid, maxrowid, maxlen

    def get_document(self, id):
        """Returns the text of a specific patient record given the ID (row ID in NOTEEVENTS).
        """
        text = ""
        self.cur.execute("select TEXT from mimic.NOTEEVENTS where ROW_ID = %d" % id)
        text = self.cur.fetchall()
        return text[0][0]

    def get_all_patient_document_ids(self, patientID):

        """Returns a list of all document IDs associated with patientID.
        """
        records = []
        self.cur.execute("select ROW_ID from mimic.NOTEEVENTS where SUBJECT_ID = %d" % patientID)
        records = self.cur.fetchall()
        return flatten(records)

    def list_all_patient_ids(self):
        """Returns a list of all patient IDs in the database.
        """
        ids = []
        self.cur.execute("select SUBJECT_ID from mimic.PATIENTS")
        ids = self.cur.fetchall()
        return flatten(ids)

    def list_all_document_ids(self):

        """Returns a list of all document IDs in the database.
        """
        ids = []
        self.cur.execute("select ROW_ID from mimic.NOTEEVENTS")
        ids = self.cur.fetchall()
        return flatten(ids)

    def get_document_sents(self, docID):

        """Returns list of sentences in a record.
        """
        self.cur.execute("select TEXT from mimic.NOTEEVENTS where ROW_ID = %d" % docID)
        raw = self.cur.fetchall()
        sent_list = sent_tokenize(raw[0][0])
        if not sent_list:
            print("No document text found.")
        return sent_list

    def get_abbreviations(self, doc_id):
        ''' Returns a list of the abbreviations in a document.
        '''
        sent_list = self.get_document_sents(doc_id)
        abb_list = set()
        for sent in sent_list:
            for word in word_tokenize(sent):
                pattern = r'[A-Z]{2}'
                if re.match(pattern, word):
                    abb_list.add(word)

        return list(abb_list)

    def get_abbreviation_sent_ids(self, doc_id):
        ''' Returns a list of the abbreviations in a document along with the sentence ID they appear in
            in the format [(abbreviation, sent_id), ...]
        '''

        sent_list = self.get_document_sents(doc_id)
        abb_list = []
        for i, sent in zip(range(0, len(sent_list)), sent_list):
            for word in word_tokenize(sent):
                pattern = r'[A-Z]{2}'
                if re.match(pattern, word):
                    abb_list.append((word, i))

        return list(abb_list)


    def get_documents_d(self, date):
        """Returns a list of all document IDs recorded on date. Format of YYYY-MM-DD for date.
        """
        ids = []
        self.cur.execute("select ROW_ID from mimic.NOTEEVENTS where CHARTDATE = \"%s\"" % date)
        ids = self.cur.fetchall()
        if not ids:
            print("No values returned. Note that date must be formatted YYYY-MM-DD.")
        return flatten(ids)

    def get_documents_q(self, query, n = -1):
        """returns a List of all document IDs that include this text:”Service: SURGERY”
            when n = -1, search against all getDocuments
        """
        query = "%"+query+"%"
        ids = []
        if n == -1:
            self.cur.execute("select ROW_ID from mimic.NOTEEVENTS where TEXT like \'%s\'" %query)
        else:
            self.cur.execute("select ROW_ID from mimic.NOTEEVENTS where TEXT like \'%s\' limit %d" %(query,n))
        ids = self.cur.fetchall() #tuples?, TODO: try Dict Server?
        if not ids:
            print("No values returned. Note that the query must be formatted such as Service: Surgery")
        return flatten(ids)

    def get_documents_icd9_alt(self,query):
        '''
        returns: documents in DIAGNOSES_ICD given icd 9 Code query
        dependancy: does not depend on calling get_patients
        '''
        query = "%"+str(query)+"%"
        self.cur.execute("select ROW_ID, ICD9_CODE from mimic.DIAGNOSES_ICD where ICD9_CODE like '%s'" %query)
        raws = self.cur.fetchall()
        docs = []
        for raw in raws:
            print(raw)#debug
            if raw[1][0] != 'V' or raw[1][0] != 'E':
                modified = raw[1][0:3]+'.'+raw[1][3:]

            else:
                modified = raw[1][0:2]+'.'+raw[1][2:]
            print(modified)#debug
            rt = tree.find(modified).parent
            description = rt.description
            docs.append((raw[0],rt,description))


        if not docs:
            print("No values returned.")
        return docs

    def get_documents_icd9(self,code):
        '''
        returns: documents in DIAGNOSES_ICD given icd 9 Code query
        dependancy: does not depend on calling get_patients
        '''
        code = str(code)
        self.cur.execute("select ROW_ID from mimic.DIAGNOSES_ICD where ICD9_CODE = '%s'" % code)
        ids = self.cur.fetchall()
        if not ids:
            print("No values returned.")
            return None
        self.cur.execute("select SHORT_TITLE from mimic.D_ICD_DIAGNOSES where ICD9_CODE ='%s'" % code)

        d = {code: (flatten(self.cur.fetchall()), flatten(ids))}

        return d

    def get_prescription(self):
        """ TODO: NEEDS TO BE FIXED. CURRENTLY HAS IDs HARDCODED IN.
        """
        for patient in self.patients.values():
            self.cur.execute("select DRUG from mimic.PRESCRIPTIONS where ROW_ID = 2968759 or ROW_ID = 2968760")
            drugtuple = self.cur.fetchall()
            druglist = []
            for drug in drugtuple:
                druglist.append(drug[0])
            patient.addPrescriptions(druglist)

    def count_all_prescriptions(self):
        """ Returns a dictionary with each medicine in PRESCRIPTIONS as keys
            and how many times it has been prescribed as values. Takes a long time to run.
        """
        meds_dict = {}
        self.cur.execute("select DRUG from mimic.PRESCRIPTIONS")
        raw = self.cur.fetchall()
        meds_list = flatten(raw)
        for med in meds_list:
            if med in meds_dict:
                meds_dict[med] += 1
            else:
                meds_dict[med] = 1

        return meds_dict

    def get_diagnoses(self):
        """Adds diagnoses (converted from ICD-9 code) from DIAGNOSES_ICD to patient.diagnoses for each patient in patients dictionary.
        """
        codes = []
        diags = {}
        for patient in self.patients.values():
            self.cur.execute("select ICD9_CODE from mimic.DIAGNOSES_ICD where SUBJECT_ID = %d" % patient.id)
            codes = self.cur.fetchall()
            for code in codes:
                if code not in diags:
                    self.cur.execute("select LONG_TITLE from mimic.D_ICD_DIAGNOSES where ICD9_CODE = \"%s\"" % code)
                    diags[code] = self.cur.fetchall()
                patient.diagnose(diags[code])

    def get_procedures(self):
        """Adds procedures (converted from ICD-9 code) from PROCEDURES_ICD to patient.procedures for each patient in patients dictionary.
        """
        codes = []
        procs = {}
        for patient in self.patients.values():
            self.cur.execute("select ICD9_CODE from mimic.PROCEDURES_ICD where SUBJECT_ID = %d" % patient.id)
            codes = self.cur.fetchall()
            for code in codes:
                if code not in procs:
                    self.cur.execute("select LONG_TITLE from mimic.D_ICD_PROCEDURES where ICD9_CODE = \"%s\"" % code)
                    procs[code] = self.cur.fetchall()
                patient.add_procedure(procs[code])

    def extract_patient_words(self, patientID):
        """Uses Gensim to extract all words relevant to a patient and writes these words to a file [patientID].txt.
        """

        # will hold all text to be processed by gensim
        text = []

        if patientID in self.patients:
            patient = self.patients[patientID]

            # Adds note_events to text
            if not patient.note_events:
                self.get_note_events()
            for doc in patient.note_events:
                text.extend(doc[1])

            # Adds prescriptions to text
            if not patient.prescriptions:
                self.get_prescription()
            text.extend(patient.prescriptions)

            # # Adds diagnoses to text
            # if not patient.diagnosis:
            #     self.get_diagnoses()
            # text.extend([diagnosis.name for diagnosis in patient.diagnosis])

            # # Adds procedures to text
            # if not patient.procedures:
            #     self.get_procedures()
            # text.extend([procedure.name for procedure in patient.procedures])

        ### Cleans the documents of punctuation ###
        text = [sent.translate(str.maketrans('', '', string.punctuation)) for sent in text]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(text)
        names = vectorizer.get_feature_names()
        doc = 0
        feature_index = tfidf_matrix[doc,:].nonzero()[1]
        scores = zip(feature_index, [tfidf_matrix[doc, x] for x in feature_index])

        print("TEMPORARY OUTPUT FOR TASK T4.4")
        for w, s in [(names[i], s) for (i, s) in scores]:
            print(w, s)
        return scores
    def extract_key_words(self, text):
        # code from AAN Keyword Cloud
        def remove_common_words_and_count(tokens):
            common_words = {'figure','a','able','about','above','abroad','according','accordingly','across','actually','adj','after','afterwards','again','against','ago','ahead','ain\'t','all','allow','allows','almost','alone','along','alongside','already','also','although','always','am','amid','amidst','among','amongst','an','and','another','any','anybody','anyhow','anyone','anything','anyway','anyways','anywhere','apart','appear','appreciate','appropriate','are','aren\'t','around','as','a\'s','aside','ask','asking','associated','at','available','away','awfully','b','back','backward','backwards','be','became','because','become','becomes','becoming','been','before','beforehand','begin','behind','being','believe','below','beside','besides','best','better','between','beyond','both','brief','but','by','c','came','can','cannot','cant','can\'t','caption','cause','causes','certain','certainly','changes','clearly','c\'mon','co','co.','com','come','comes','concerning','consequently','consider','considering','contain','containing','contains','corresponding','could','couldn\'t','course','c\'s','currently','d','dare','daren\'t','definitely','described','despite','did','didn\'t','different','directly','do','does','doesn\'t','doing','done','don\'t','down','downwards','during','e','each','edu','eg','eight','eighty','either','else','elsewhere','end','ending','enough','entirely','especially','et','etc','even','ever','evermore','every','everybody','everyone','everything','everywhere','ex','exactly','example','except','f','fairly','far','farther','few','fewer','fifth','first','five','followed','following','follows','for','forever','former','formerly','forth','forward','found','four','from','further','furthermore','g','get','gets','getting','given','gives','go','goes','going','gone','got','gotten','greetings','h','had','hadn\'t','half','happens','hardly','has','hasn\'t','have','haven\'t','having','he','he\'d','he\'ll','hello','help','hence','her','here','hereafter','hereby','herein','here\'s','hereupon','hers','herself','he\'s','hi','him','himself','his','hither','hopefully','how','howbeit','however','hundred','i','i\'d','ie','if','ignored','i\'ll','i\'m','immediate','in','inasmuch','inc','inc.','indeed','indicate','indicated','indicates','inner','inside','insofar','instead','into','inward','is','isn\'t','it','it\'d','it\'ll','its','it\'s','itself','i\'ve','j','just','k','keep','keeps','kept','know','known','knows','l','last','lately','later','latter','latterly','least','less','lest','let','let\'s','like','liked','likely','likewise','little','look','looking','looks','low','lower','ltd','m','made','mainly','make','makes','many','may','maybe','mayn\'t','me','mean','meantime','meanwhile','merely','might','mightn\'t','mine','minus','miss','more','moreover','most','mostly','mr','mrs','much','must','mustn\'t','my','myself','n','name','namely','nd','near','nearly','necessary','need','needn\'t','needs','neither','never','neverf','neverless','nevertheless','new','next','nine','ninety','no','nobody','non','none','nonetheless','noone','no-one','nor','normally','not','nothing','notwithstanding','novel','now','nowhere','o','obviously','of','off','often','oh','ok','okay','old','on','once','one','ones','one\'s','only','onto','opposite','or','other','others','otherwise','ought','oughtn\'t','our','ours','ourselves','out','outside','over','overall','own','p','particular','particularly','past','per','perhaps','placed','please','plus','possible','presumably','probably','provided','provides','q','que','quite','qv','r','rather','rd','re','really','reasonably','recent','recently','regarding','regardless','regards','relatively','respectively','right','round','s','said','same','saw','say','saying','says','second','secondly','see','seeing','seem','seemed','seeming','seems','seen','self','selves','sensible','sent','serious','seriously','seven','several','shall','shan\'t','she','she\'d','she\'ll','she\'s','should','shouldn\'t','since','six','so','some','somebody','someday','somehow','someone','something','sometime','sometimes','somewhat','somewhere','soon','sorry','specified','specify','specifying','still','sub','such','sup','sure','t','take','taken','taking','tell','tends','th','than','thank','thanks','thanx','that','that\'ll','thats','that\'s','that\'ve','the','their','theirs','them','themselves','then','thence','there','thereafter','thereby','there\'d','therefore','therein','there\'ll','there\'re','theres','there\'s','thereupon','there\'ve','these','they','they\'d','they\'ll','they\'re','they\'ve','thing','things','think','third','thirty','this','thorough','thoroughly','those','though','three','through','throughout','thru','thus','till','to','together','too','took','toward','towards','tried','tries','truly','try','trying','t\'s','twice','two','u','un','under','underneath','undoing','unfortunately','unless','unlike','unlikely','until','unto','up','upon','upwards','us','use','used','useful','uses','using','usually','v','value','various','versus','very','via','viz','vs','w','want','wants','was','wasn\'t','way','we','we\'d','welcome','well','we\'ll','went','were','we\'re','weren\'t','we\'ve','what','whatever','what\'ll','what\'s','what\'ve','when','whence','whenever','where','whereafter','whereas','whereby','wherein','where\'s','whereupon','wherever','whether','which','whichever','while','whilst','whither','who','who\'d','whoever','whole','who\'ll','whom','whomever','who\'s','whose','why','will','willing','wish','with','within','without','wonder','won\'t','would','wouldn\'t','x','y','yes','yet','you','you\'d','you\'ll','your','you\'re','yours','yourself','yourselves','you\'ve','z','zero'}
            token_counts = {}
            for token in tokens:
                token = token.lower()
                if token in common_words or token.isdigit() or len(token) == 1:
                    pass
                elif token in token_counts:
                    token_counts[token] += 1
                else:
                    token_counts[token] = 1
            return token_counts
        token_counts = remove_common_words_and_count(re.findall('[\w\-]+', text))
        # Sort token with highest counts first, and take top 50 only.
        sorted_token_counts = sorted(token_counts.items(), key=lambda x: x[1], reverse=True)[:50]
        scale = 48.0 / sorted_token_counts[0][1]
        # Normalize font size for each token such that token with largest count is size 48.
        token_to_font_size = [(tup[0], round(tup[1] * scale, 1)) for tup in sorted_token_counts]
        return sorted_token_counts


    def extract_phrases(self, docID):
        self.cur.execute("SELECT TEXT FROM mimic.NOTEEVENTS WHERE ROW_ID = %d" % docID)
        doc = self.cur.fetchall()
        upperdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        f = open(upperdir+"/external/phrase-at-scale/data/raw_doc.txt", "w+")
        f.write(doc[0][0])
        f.close()

        cmd = '~/venv/lib/python3.6/site-packages/pyspark/bin/spark-submit --master local[200] --driver-memory 4G external/phrase-at-scale/phrase_generator.py'
        os.system(cmd)

    def output_note_events_file_by_patients(self, directory):
        '''
        input: file path like MedGen/output/patients
        return: none
        output: Noteevents Text fields saved in MedGen/output/patients/patient[SUBJECT_ID]/[ROW_ID].txt files
        '''

        #self.cur.execute('select SUBJECT_ID, count(ROW_ID) from mimic.NOTEEVENTS group by SUBJECT_ID having count(ROW_ID) > 10 limit 1')
        self.cur.execute('select SUBJECT_ID, count(ROW_ID) from (select SUBJECT_ID, ROW_ID from mimic.NOTEEVENTS limit 10000) as SMALLNE group by SUBJECT_ID having count(ROW_ID) > 10 limit 10')
        patients = self.cur.fetchall()
        print('Format: (Patient ID, Document count) \n', patients)
        for patient in patients:
            pid = patient[0]
            print('patient %d' %pid)
            self.cur.execute('select ROW_ID from (select SUBJECT_ID, ROW_ID from mimic.NOTEEVENTS limit 10000) as SMALLNE where SUBJECT_ID = %d' %pid)
            docids = self.cur.fetchall()
            for num,doctup in enumerate(docids, start = 1):
                docid = doctup[0]
                self.cur.execute('select TEXT from mimic.NOTEEVENTS where ROW_ID = %d' %docid)
                doctext = self.cur.fetchall()
                try:
                    os.makedirs(directory+'patient%d' %pid)
                    docpath = os.path.join(directory, 'patient%d' %pid)
                except FileExistsError:
                    docpath = os.path.join(directory, 'patient%d' %pid)
                with open(os.path.join(docpath, '%d.txt' %docid), 'w+') as f:
                    f.write(doctext[0][0])
                print('patient document %d saved' %docid)
        print('Done, please check MedGen/Output/patients/ for files')

    def output_note_events_discharge_summary(self, directory):
        '''
        input: file path like MedGen/output/
        return: none
        output: Noteevents Text fields saved in MedGen/output/discharge_summary/[ROW_ID].txt files
        '''

        #self.cur.execute('select SUBJECT_ID, count(ROW_ID) from mimic.NOTEEVENTS group by SUBJECT_ID having count(ROW_ID) > 10 limit 1')
        self.cur.execute("select ROW_ID, TEXT from (select * from mimic.NOTEEVENTS limit 10000) as SMALLNE where CATEGORY = 'Discharge summary' limit 100")
        raw = self.cur.fetchall()
        for doc in raw:
            docid = doc[0]
            doctext = doc[1]
            print('Discharge Summary %d' %docid)
            try:
                os.makedirs(directory)
                docpath = directory
            except FileExistsError:
                docpath = directory
            with open(os.path.join(docpath, '%d.txt' %docid), 'w+') as f:
                f.write(doctext)
                print('discharge summary %d saved' %docid)
        print('Done, please check MedGen/output/discharge_summary for files')

    def outputAbbreviation(self, directory):
        '''
        input: file path like MedGen/output/
        return: none
        output: Noteevents Text files containing abbreviation “AB” in e.g. MedGen/output/AB/194442.txt
        '''


    def count_gender(self, gender):
        ''' Counts how many patients there are of a certain gender in the database.
            Argument gender must be a capitalized single-letter string.
        '''

        self.cur.execute('SELECT COUNT(*) FROM mimic.PATIENTS WHERE GENDER = \'%s\'' % gender)
        count = self.cur.fetchall()

        return count[0][0]

    def docs_with_phrase(self, phrase):
        ''' Writes document text containing phrase to files named with document IDs.
        '''

        self.cur.execute('SELECT ROW_ID, TEXT FROM mimic.NOTEEVENTS WHERE TEXT LIKE \'%%%s%%\' LIMIT 1' % phrase)
        docs = self.cur.fetchall()
        os.mkdir("docs_with_phrase_%s" % phrase)

    #TODO: bert tokenize
    def get_bert_tokenize(self, doc_id):
        text = self.get_document(doc_id)
        tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
        bert_tokenized_text = tokenizer.tokenize(text)
        return bert_tokenized_text

    # TODO: bart sumamrize test
    def summarize_huggingface(self, text, model_name):
        if '/' in model_name:
            path = model_name.split('/')[1]
        else:
            path = model_name

        tokenizer_path = os.path.join(os.path.dirname(__file__), '../..', 'huggingface', path, 'tokenizer')
        model_path = os.path.join(os.path.dirname(__file__), '../..', 'huggingface', path, 'model')
        tokenizer = AutoTokenizer.from_pretrained('t5-small', cache_dir=tokenizer_path)
        model = AutoModelWithLMHead.from_pretrained(model_name, cache_dir=model_path)

        inputs = tokenizer([text], max_length=1024, return_tensors='pt')
        # early_stopping=True produces shorter summaries. Changing max_ and min_length doesn't change anything.
        summary_ids = model.generate(inputs['input_ids'], num_beams=4, max_length=inputs['input_ids'].shape[1], early_stopping=False)
        summary = [tokenizer.decode(g, skip_special_tokens=True, clean_up_tokenization_spaces=False) for g in summary_ids]
        summary = " ".join(summary)
        return summary

    def bert_predict_masked(self, doc_id, sentence_id, mask_id):
        #TODO: FROM HUGGINGFACE LIBRARY
        tokenizer = AutoTokenizer.from_pretrained("bert-large-uncased-whole-word-masking")
        model = AutoModelWithLMHead.from_pretrained("bert-large-uncased-whole-word-masking")

        kit_doc = self.get_document_sents(doc_id) #retrieve that doc
        sentence = kit_doc[sentence_id] #choose that particular sentence
        #print(sentence)

        #TODO: replace a random word by a masked symbol
        sentence_list = sentence.split(' ')
        sentence_list[mask_id] = tokenizer.mask_token
        sequence = ' '.join(sentence_list)

        input = tokenizer.encode(sequence, return_tensors="pt")
        mask_token_index = torch.where(input == tokenizer.mask_token_id)[1]

        token_logits = model(input)[0]
        mask_token_logits = token_logits[0, mask_token_index, :]

        top_token = torch.topk(mask_token_logits, 1, dim=1).indices[0].tolist()

        for token in top_token:
            return sequence.replace(tokenizer.mask_token, tokenizer.decode([token]))

    def close_session(self):
        """Ends DB Session by closing SSH
        Tunnel and MySQL database connection.
        """
        #self.server.stop()
        self.cnx.close()

### ---------------- ###
### HELPER FUNCTIONS ###
### ---------------- ###

def start_session(db_user, db_pass):
    """Opens SQL Connection. Creates cursor
    for executing queries. Returns ehr_db object.

    Args:

        db_user (str): Username for MySQL DB on Tangra
        db_pass (str): Password for MySQL DB on Tangra

    Returns:
        dict: Contains SSHTunnelForwarder, pymysql connection, and
        pymysql cursor objects.
    """


    cnx = pymysql.connect(host='localhost',
                             user=db_user,
                             password=db_pass,port = 3306)
                             #port=8080)
    # Session Dictionary: Stores SSH Tunnel (server), MySQL Connection (cnx),
    # and DB Cursor(cursor).
    #sess_dict = {'server': server, 'cnx':cnx, 'cur':cnx.cursor()}
    sess_dict = {'cnx':cnx, 'cur':cnx.cursor()}
    # Create Session Object:
    sess = ehr_db(sess_dict)

    sess.cur.execute("use mimic")

    return sess

def createPatient(data):
    """Creates a single Patient object.

    Args:
        data (dict): Dictionary containing patient data

    Returns:
        patient: Patient object
    """
    data["diagnosis"] = getDiagnoses(data["id"], current=True)
    data["current_prescriptions"] = getMeds(data["id"], current=True)
    history = medicalHistory(data["id"])
    data["past_prescriptions"] = history["past_prescriptions"]
    data["past_diagnoses"] = history["past_diagnoses"]
    data["procedures"] = history["procedures"]

    patient = Patient(data)

    return patient

def flatten(lst):
    """Returns flattened list from nested list.
    """
    if not lst: return lst
    return [x for sublist in lst for x in sublist]

def numbered_print(lst):
    for num, elt in enumerate(lst, start = 1):
        print(num, '\n', elt)


# def init_embedding_model():
#     train_word2vec()

def get_abbs_sent_ids(text):
    ''' Returns a list of the abbreviations in a document along with the sentence ID they appear in
        in the format [(abbreviation, sent_id), ...]
    '''
    sent_list = sent_tokenize(text)
    abb_list = []
    for i, sent in zip(range(0, len(sent_list)), sent_list):
        for word in word_tokenize(sent):
            pattern = r'[A-Z]{2}'
            if re.match(pattern, word):
                abb_list.append((word, i))

    return list(abb_list)
def post_single_dict_to_solr(d: dict, core: str) -> None:
    response = requests.post('http://tangra.cs.yale.edu:8983/solr/{}/update/json/docs'.format(core), json=d)

def abbs_disambiguate(ABB):
    long_forms, long_form_to_score_map = get_solr_response_umn_wrap(ABB)
    return long_forms

def get_documents_solr(query):
    ids, scores = get_solr_response_mimic(query)
    if not ids:
        print("No documents found")
    return sorted(ids)



### ------------------- ###
### Tangra DB Structure ###
### ------------------- ###

### DIAGNOSES_ICD Table ###
# Description: Stores ICD-9 Diagnosis Codes for patients
# Source: https://mimic.physionet.org/mimictables/diagnoses_icd/
# ATTRIBUTES:
# HADM_ID = unique ID for hospital ID (possibly more than 1 per patient)
# SEQ_NUM = Order of priority for ICD diagnoses
# ICD9_CODE = ICD-9 code for patient diagnosis
# SUBJECT_ID = unique ID for each patient

### D_ICD_DIAGNOSES Table ###
# Description: Definition Table for ICD Diagnoses
# Source: https://mimic.physionet.org/mimictables/d_icd_diagnoses/
# ATTRIBUTES:
# SHORT_TITLE
# LONG_TITLE
# ICD9_CODE: FK on DIAGNOSES_ICD.ICD9_CODE

### D_ICD_PROCEDURES Table ###
# Description: Definition Table for ICD procedures
# Source: https://mimic.physionet.org/mimictables/d_icd_procedures/
# ATTRIBUTES:
# SHORT_TITLE
# LONG_TITLE
# ICD9_CODE: FK on DIAGNOSES_ICD.ICD9_CODE

### NOTEEVENTS Table ###
# Description: Stores all notes for patients
# Source: https://mimic.physionet.org/mimictables/noteevents/
# ATTRIBUTES:
# SUBJECT_ID = unique ID for patient
# HADM_ID = unique hospital admission ID
# CHART-DATE = timestamp for date when note was charted
# CATEGORY and DESCRIPTION: describe type of note
# CGID = unique ID for caregiver
# ISERROR = if 1, means physician identified note as erroneous
# TEXT = note text

### PATIENTS Table ###
# Description: Demographic chart data for all patients
# Source: https://mimic.physionet.org/mimictables/patients/
# ATTRIBUTES:
# SUBJECT_ID = unique ID for patient
# GENDER
# DOB
# DOD_HOSP: Date of death as recorded by hospital (null if alive)
# DOD_SSN: Date of death as recorded in social security DB. (null if alive)
# DOD_HOSP takes priority over DOD_SSN if both present
# EXPIRE_FLAG = 1 if patient dead

### PROCEDURES_ICD Table ###
# Description: Stores ICD-9 procedures for patients (similar to DIAGNOSES_ICD)
# Source: https://mimic.physionet.org/mimictables/procedures_icd/
# ATTRIBUTES:
# SUBJECT_ID = unique patient ID
# HADM_ID = unique hospital admission ID
# SEQ_NUM = order in which procedures were performed
# ICD9_CODE = ICD-9 code for procedure
