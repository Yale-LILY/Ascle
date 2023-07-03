import mimiciii
import pymysql


# Replace the placeholders with your MySQL database credentials
host = 'localhost'
USERNAME = 'root'
PASSWORD = 'Ilove4xwz!'
database = 'mimiciiiv14'


# these are mimic-iii parameters
# DOC_ID = 1354526  # Temporary!!!
#
# # Number of documents in NOTEEVENTS.
# NUM_DOCS = 2083180
#
# # Number of patients in PATIENTS.
# NUM_PATIENTS = 46520
#
# # Number of diagnoses in DIAGNOSES_ICD.
# NUM_DIAGS = 823933

# Establish the connection
connection = pymysql.connect(host=host, user=USERNAME, password=PASSWORD, database=database, port=3306)

# import pdb;pdb.set_trace()

# Create a cursor object to execute SQL queries
cursor = connection.cursor()

# Execute a SELECT query
query = "select count(*) from PATIENTS"
cursor.execute(query)

# Fetch and print the results
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor and connection
cursor.close()
connection.close()


# get the mysql session
ehrdb = mimiciii.start_session(USERNAME, PASSWORD)

# get three patient records
ehrdb.get_patients(3)

# show the gender of the patient with ID 249
print (ehrdb.patients[249].sex)

# get a note
doc_id = 20
print('Kit function printing a numbered list of all sentences in document %d' % doc_id)
# MIMIC EHRs are very messy and sentence tokenizaton often doesn't work
kit_doc = ehrdb.get_document_sents(doc_id)
mimiciii.numbered_print(kit_doc)

ehrdb.cur.execute("select TEXT from mimic.NOTEEVENTS where ROW_ID = %d " % doc_id)
raw = ehrdb.cur.fetchall()
test_doc = mimiciii.sent_tokenize(raw[0][0])
print(test_doc)


# simple search
query = "Service: SURGERY"
print('Printing a list of all document ids including query like ', query, 'this may take some time...')
kit_ids = ehrdb.get_documents_q(query)
print(kit_ids[:30])  # Extremely long list of DOC_IDs
print("...")

query = "%" + query + "%"
ehrdb.cur.execute("select ROW_ID from mimic.NOTEEVENTS where TEXT like \'%s\'" % query)
raw = ehrdb.cur.fetchall()
test_ids = mimiciii.flatten(raw)