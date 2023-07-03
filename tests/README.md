## What's new?

1. The UMN Clinical Abbreviation Sense Inventory: Clinical Abbreviations and Acronyms is indexed to solr core ehr_abbreviations (440 most frequently used abbreviations, 30000+ docs in total on solr)

The following two are temporarily placed in sample_script.py only, yet to incorporate into test.py
2. Function to output discharge summaries for patients who have more then 10 of them
3. Function to initialize word2vec model using outputted discharge summary above

## Running Unit Tests on MIMIC-III:

Running test.py without any arguments would run all tests ones but **skips** ones that take a while to run. (Those tests must be called explicitly.)
```
> python tests.py
```

To run specific tests, follow the format python tests.py CLASS_NAME1.TEST_NAME1 CLASS_NAME2.TEST_NAME2 …
For example, you can run
```
> python tests.py t7.test7_1_naive_bayes

```
or
```
> python tests.py t3.test3_4_doc_sentences t7.test7_1_naive_bayes 
```

Unittest prints "." when a test runs successfully, "E" when it encounters an error, and "s" when it skips a test.

No tests updates the database; all of them are just processing information from it. Not all tests currently work.

###Tests available to run

The tests marked in bold are skipped and must be run explicitly.

T1.
1. Count the total number of patients. test1_1_count_patients
2. **Count the total number of patient records** (fails). test1_2_count_docs
3. **Count the number of sentences**. test1_3_note_info
4. **Print the record with the most sentences**. test1_4_longest_note

T2.

1. Display a full document given its document ID. test2_1_print_note
2. **Count how many documents are associated with a given patient, given the patient ID, e.g., 23224 - show also the list of document IDs**. test2_2_patient_info
3. List all document IDs. test2_3_doc_ids
4. List all patient IDs. test2_4_patient_ids
5. List all document IDs for a given admission date, e.g., 2188-11-1. test2_5_docs_on_date

T3.

1. Extract all abbreviations from a document, given the document ID. For now, let’s assume that an abbreviation is a sequence of two or more capital letters, e.g., GERD, PEERL, AMI. test3_1_extract_abbrevations
2. **List all document IDs that include keyword "meningitis"**. test3_2_docs_with_query
3. **List all document IDs that include keywords "Service: SURGERY”**. test3_3_query_docs
4. Given a document ID, show a numbered list of all sentences in that document. test3_4_doc_sentences
5. **Count the number of prescriptions for each unique medication**. test3_5_medications

T5

1. **Use https://github.com/kavgan/phrase-at-scale to extract phrases from a document, given its ID**. test5_1_extract_phrases
2. Count how many patients are labeled as “male” or “female”. test5_2_count_gender

T6
1. **Classifies the sentiment of a document as positive or negative using AllenNLLP.** test6_1_sentiment_classification
2. **Performs named entity recognition on a document using AllenNLLP**. test6_2_ner
3. **Tokenizes the words of a document using Huggingface.** test6_3_tokenize

T7. 
1. **Creates extractive summary of an EHR with Naive Bayes Algorithm trained on PubMed articles.** test7_1_naive_bayes
2. **Generates abstractive summary of an EHR with pre-trained Distilbart model from Huggingface (works poorly)**. test7_2_distilbart_summary
3. **Generates abstractive summary of an EHR with pre-trained T5 model from Huggingface (works poorly)**. test7_3_t5_summary