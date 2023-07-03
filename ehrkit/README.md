# EHRKit Documentation
## Directory Structure
* EHRKit
  * ehrkit
    * ehrkit.py
    * solr_lib.py
    * classes.py
  * external
    * icd9
      * status: incorporated but doesn't seem useful
    * patient2vec
      * status: not yet incorporated
      * could be useful:
    * phrase-at-scale
      * status: incorporated, but only a crude version
      * problem: does not return the phrases but outputs it to files
  * scripts
    * helper scripts for handling data
    * see README_scripts for more descriptions
  * tests
    * see README_tests for more descriptions

## ehrkit.py functions
* helper functions:
  * *def start_session(db_user, db_pass): -> dict*:
  * *def createPatient(data):*
  * *def flatten(lst):*
  * *def numbered_print(lst):*
  * *def init_embedding_model():*
  * *def get_abbs_sent_ids(text):*
  * *def post_single_dict_to_solr(d: dict, core: str)-> None*
  * *def abbs_disambiguate(ABB):*
  * *def get_documents_solr(query):*

* *class ehr_db*
  * attributes:
    * *cnx* -- MySQL connection object
    * *cur* -- MySQL cursor
    * *patients = {}* -- Patient (from classes.py) dictionary
  * methods:
    * *def close_session(self):*
    * *def get_patients(self, n):*
    * *def count_patients(self):*
    * *def count_gender(self, gender):*
    * *def count_docs(self, query, getAll = False, inverted = False):*
    * *def get_note_events(self):*
    * *def longest_NE(self):*
    * *def get_document(self, id):*
    * *def get_all_patient_document_ids(self, patientID):*
    * *def list_all_patient_ids(self):*
    * *def list_all_document_ids(self):*
    * *def get_document_sents(self, docID):*
    * *def get_abbreviations(self, doc_id):*
    * *def get_abbreviation_sent_ids(self, doc_id):*
    * *def get_documents_d(self, date):*
    * *def get_documents_q(self, query, n = -1):*
    * *def get_documents_icd9_alt(self,query):*
    * *def get_documents_icd9(self,code):*
    * *def get_prescription(self):*
    * *def extract_key_words(self, text):*
    * *def count_all_prescriptions(self):*
    * *def get_diagnoses(self):*
    * *def get_procedures(self):*
    * *def extract_patient_words(self, patientID):*
    * *def output_note_events_file_by_patients(self, directory):*
    * *def output_note_events_discharge_summary(self, directory):*

  * yet to refactor:
    * *def extract_key_words(self, text):*
    * *def get_abbreviations(self, doc_id):*
    * *def get_abbreviation_sent_ids(self, doc_id):*
  * unfinished:
    * *def docs_with_phrase(self, phrase):*
    * *def outputAbbreviation(self, directory):*
    * *def extract_phrases(self, docID):*
