# Individual Task Examples

In this folder, you can test individual tasks including ICD9 code classification, Naive Bayes summarization, and query extraction.

Task Details:
- [ICD9 code classification](https://github.com/Yale-LILY/EHRKit/tree/master/mimic_icd9_coding): predict ICD9 code using tfidf representations
- [Naive Bayes Summarization](https://github.com/Yale-LILY/EHRKit/tree/master/summarization/pubmed_summarization): summarize text using a Naive Bayes model trained on the PubMed corpus
- [Query Extraction](https://github.com/Yale-LILY/EHRKit/tree/master/QueryExtraction): search for specific queries in medical text using different methods

## Virtual Environment
Create virtual environment in parent directory using the following commands.
```sh
cd ..
python3 -m venv ehrvir/
source ehrvir/bin/activate
```
If you are using pip==18.1, comment out line 20 of requirements.txt ```en-core-web-sm``` and run 
```sh
pip install -r requirements.txt
```
Install ```en-core-web-sm``` by running
```sh
python -m spacy download en_core_web_sm
```
This is needed for the entity extraction task.

## Preparation
Create MIMIC data and output data directory using the following commands.
```sh
mkdir data
mkdir data/mimic_data
mkdir data/output_data
```
You will need to put all MIMIC data under ```data/mimic_data```, which is the folder containing all csv files downloaded from the orginal MIMIC dataset. If you are on tangra, you can the following command to copy everything from ```/lada2/lily/zl379/Year4/EHRTest/EHRKit/tutorials/data/mimic_data```:
```sh 
cp -r /lada2/lily/zl379/Year4/EHRTest/EHRKit/tutorials/data/mimic_data data/.
```

## Run mimic_classifier.py
```sh
cp mimic_classifier.py ../.
cd ..
python mimic_classifier.py
```
Note: you need to run ```mimic_classifier.py``` from the ROOT path of EHRKit.

## Run a notebook
You can test Naive Bayes summarization and query extraction using the notebooks naiveBayes.ipynb and query_extractor respectively. ICD0 code classification is also documented in mimic\_classifier.ipynb.

To run a notebook, you need to first install ipykernel using ```python -m pip install ipykernel```. Set tthe kernel name to your virtual environment name using ```ipython kernel install --user --name=<name of virtual environment>```. Run ```jupyter notebook --no-browser . &``` and note the server port number. Open a local terminal and run ```ssh -o ServerAliveInterval=30  -L <any local port>:localhost:<server port number> <username>@tangra.cs.yale.edu```. Go to http://localhost:localportnumber and follow instructions in the notebook. 

## Collated tasks
Instructions to run other tasks are located in the [collated_tasks](https://github.com/Yale-LILY/EHRKit/tree/master/collated_tasks) directory.
