# MedGen - Query and Search, Support for MIMIC-III

## Quick Start
### Data Preperation
[Mysql](https://www.mysql.com) is need to run these functions. Please make sure it is running, and you know the username and password. You will need them later. 

Once you download the [mimic-iii](https://physionet.org/content/mimiciii/) data, you will get a list of `.csv` files, we provide the `build_db.sql` to build the database from these csv files, run the following:

```mysql -u <username>> -p -h "localhost" mimiciiiv14 < build_db.sql ```

In the `build_db.sql`, make sure the data file paths are correct. Importing may take some time, after this step, you will see the `mimiciiiv14` database is built. Then you are feel to run the tests. 

### Simple Tests

```python
import mimiciii
import pymysql


# Replace the placeholders with your MySQL database credentials
host = 'localhost'
USERNAME = 'username'
PASSWORD = 'db_password'
database = 'mimiciiiv14'

# Establish the connection
connection = pymysql.connect(host=host, user=USERNAME, password=PASSWORD, database=database, port=3306)

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Execute a SELECT query from the table PATIENTS
query = "select count(*) from PATIENTS"
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()

```

Get patient instances, and obtain the gender: 

```python
import mimiciii

# get the mysql session
ehrdb = mimiciii.start_session(USERNAME, PASSWORD)

# get three patient records
ehrdb.get_patients(3)

# show the gender of the patient with ID 249
print (ehrdb.patients[249].sex)
```

Get note record with ID 20:

```python
import mimiciii

# get the mysql session
ehrdb = mimiciii.start_session(USERNAME, PASSWORD)
doc_id = 20
print('Kit function printing a numbered list of all sentences in document %d' % doc_id)
# MIMIC EHRs are very messy and sentence tokenizaton often doesn't work
kit_doc = ehrdb.get_document_sents(doc_id)
mimiciii.numbered_print(kit_doc)
```

Query from the notes based on key terms: 

```python
# find some notes that mentioned "Service: SURGERY"
query = "Service: SURGERY"
print('Printing a list of all document ids including query like ', query, 'this may take some time...')
kit_ids = ehrdb.get_documents_q(query)
print(kit_ids[:30])  # Extremely long list of DOC_IDs
print("...")
```

A quick lightweight test is provided in `demo.py`, by running `python demo.py`. 
We also provide how to use more functions in `tests.py`. Please run `python tests.py` for more details, and this may take some time. 

## mimiciii.py functions
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


