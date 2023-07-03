# Unsupervised Extractive Summarization 

Implements a summarizers package for text summarization and evaluation. Package includes Lexrank and folder2rouge. Also implements scripts for producing batch summaries using the Lexrank package on pubmed and noteevents data, and the bert extractive summarizers pypi package on pubmed data.

## Setup

After following EHRKit installation instructions, install dependencies for this subpackage.

```
cd EHRKit/Sanya/
pip install -r requirements.txt
``` 

For folder2rouge, first setup files2rouge by following instructions here https://github.com/pltrdy/files2rouge

## Scripts

**generate_summaries.py** generates Lexrank summaries using this summarizers package for a directory of source documents.
- --train: Takes in the directory path containing training documents, which are used for calculating idf scores.
- --saveto: Takes in the directory path for saving the generated summaries (saved with the extension *name*.sum)
- --test (optional): Takes in the directory path containing documents for which to produce summaries. The default is the documents in the train directory.
- --ntrain (optional): First n number of documents to train on. Default is all documents.
- --ntest (optional): First n number of documents to produce summaries of. Default is all documents.
- --threshold (optional): Sets threshold for Lexrank algorithm. Default is 0.03.
- --size (optional): Sets size (number of sentences) of summaries produced. Default is 1.

```
> python generate_summaries.py --train /data/lily/jmg277/nc_text/source/ --saveto /data/lily/sn482/summaries
``` 


**rouge_scores.py** generates rouge score for the summaries produced using this summarizers package.
- --summaries: Takes in the directory path containing summaries in the format name.sum.
- --references: Takes in the directory path for the references of the summaries produced in the format name.tgt. Each tgt file must have same number of newlines as corresponding .sum file.
- --saveto (optional): Takes in the file path for saving the ROUGE score results.

```
> python rouge_scores.py --summaries /data/lily/sn482/summaries --references /data/lily/sn482/reference_abstracts/
``` 


**/scripts/bert_summaries.py** generates bert extractive summaries for directory containing source documents using the pypi package:
- --source: Takes in the directory path containing source documents for which to produce summaries.
- --saveto: Takes in the directory path for saving the generated summaries (saved with the extension *name*.sum)
- --n (optional): First n number of documents to produce summaries of. Default is all documents.
- --ratio (optional): Sets ratio of number of sentences in summaries wrt the source document. Default is 0.05.

```
> python bert_pubmed.py --source /data/lily/jmg277/nc_text_body/source --saveto /data/lily/sn482/pubmed_summaries/bert_script_summaries/
``` 


**/scripts/noteevents_lexrank.py** generates Lexrank summaries by note and by entire patient history for notes in MIMIC-III database using this summarizers package. 
- --saveto: Takes in the directory path for saving the generated summaries. Saved with the extension *name*.sum under script_summary_byetirehistory and script_summary_bynote. 
- --ntrain (optional): First n number of documents to train on. Default is all documents.
- --ntest (optional): First n number of documents to produce summaries of. Default is all documents.
```
> python noteevents_lexrank.py --saveto /data/lily/sn482/NOTEEVENTS_summaries
``` 

## Summarizers Package 

```
summarizers
|_ lexrank.py
|_ /evaluate
	|_ folder2rouge.py

``` 

### Lexrank 

***Initializing***

**documents:** A list of documents where each document has been parsed into a list of sentences.

**stopwords:** Set of commonly used words that the algorithm ignores. The default is the english set of words from nltk corpus.

**threshold:** Default is 0.03.

***Getting the summary***

**sentences:** Document parsed into list of sentences

**summary_size:** Number of sentences to include in the summary. Default is 1.

#### Usage


```
from summarizers import Lexrank

documents = [['This is the first document sentence 1', 'This is the first document  sentence 2'],
['This is the second document sentence 1', 'This is the second document  sentence 2']]

sentences = ['sentence 1', 'sentence 2']

lxr = Lexrank(documents, stopwords)
summary = lxr.get_summary(sentences, summary_size=10, threshold=.1)
```

### ROUGE Scores 

NOTE: The number of newlines in a summary file must match the number of newlines in the target file.

**summaries_dir:** Directory path which contains the generated summaries with the format DOC_NAME.sum

**reference_dir:** Directory path which contains the reference summaries with the format DOC_NAME.tgt

**saveto:** (optional) File path to save the ROUGE score 

#### Usage
```
from summarizers.evaluate import folder2rouge

rouge = folder2rouge(summaries_dir, reference_dir)
rouge.run(saveto=saveto_path)
```

### References

Lexrank largely derived from https://github.com/crabcamp/lexrank

folder2rouge imports files2rouge from https://github.com/pltrdy/files2rouge

bert script uses https://github.com/dmmiller612/bert-extractive-summarizer
