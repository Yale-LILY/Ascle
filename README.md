<p align="center">
   <img src="https://github.com/Yale-LILY/EHRKit/blob/v1.0/wrapper_functions/EHRLogo.png" alt="EHRKit"/>
</p>


# EHRKit: A Python Natural Language Processing Toolkit for Electronic Health Record Texts

[![Python 3.6.13](https://img.shields.io/badge/python-3.6.13-green.svg)](https://www.python.org/downloads/release/python-360/)

This library aims at processing medical texts in electronic health records. We provide specific functions to access the [MIMIC-III](https://physionet.org/content/mimiciii-demo/) record efficiently; the method includes searching by record ID, searching similar records, searching with an input query. We also support functions for some NLP tasks, including abbreviation disambiguation, extractive and abstractive summarization. For more specific evaluaiton, please check this [pre-print]([url](https://arxiv.org/abs/2204.06604)).

Moreover, if users want to deal with general medical texts, we integrate third-party libraries, including [hugginface](https://huggingface.co/), [scispacy](https://allenai.github.io/scispacy/), [allennlp](https://github.com/allenai/allennlp), [stanza](https://stanfordnlp.github.io/stanza/), and so on. Please checkout the special verison of this library, [EHRKit-WF](https://github.com/Yale-LILY/EHRKit/tree/master/wrapper_functions).

<p align="center">
   <img src="https://github.com/Yale-LILY/EHRKit/blob/v1.0/ehrkit.jpg" alt="EHRKit"/>
</p>

## Table of Contents

1. [Updates](#updates)
2. [Data](#data)
3. [Setup](#setup)
4. [Toolkit](#toolkit)
5. [Get Involved](#get-involved)
6. [Off-shelf Functions](#get-involved)
<!-- 6. [Citation](#get-involved) -->


## Updates
_24_05_2023_ - New Release Pretrained Models for Machine Translation. <br/>
_15_03_2022_ - Merged a wrapper function folder to support off-shelf medical text processing. <br/>
_10_03_2022_ - Made all tests avaiable in a ipynb file and updated the most recent version. <br/>
_12_17_2021_ - New folder collated_tasks containing Fall 2021 functionalities added <br/>
_05_11_2021_ - cleaned up the notebooks, fixed up the readme using depth=1 <br/>
_05_04_2021_ - Tests run-through added in `tests` <br/>
_04_22_2021_ - Freezing development <br/>
_04_22_2021_ - Completed the tutorials and readme. <br/>
_04_20_2021_ - Spring functionality finished -- mimic classification, summarization, and query extraction <br/>

## Data
EHRKit is built for use with Medical Information Mart for Intensive Care-III (MIMIC-III). It requires this dataset to be downloaded. This dataset is freely available to the public, but it requires completion of an online training course. Information on accessing MIMIC-III can be found at https://mimic.physionet.org/gettingstarted/access. Once this process is complete, it is recommended to download the mimic files to the folder `data/`

The other dataset that is required for some of the modules is the [pubmed dataset](https://www.ncbi.nlm.nih.gov/CBBresearch/Wilbur/IRET/DATASET/), this dataset contains a large number of medical articles. The required downloading and parsing is all performed in the `pubmed/` folder. First run `bash download_pubmed.sh` and then `python parse_articles.py`. This process is also detailed in the tutorial notebook for summarization: `tutorials/naiveBayes.ipynb`

## Setup

### Download Repository

You can download EHRKit as a git repository, simply clone to your choice of directories (keep depth small to keep the old versions out and reduce size)
```
git clone https://github.com/Yale-LILY/EHRKit.git --depth=1
```

#### Environment Option 1: using conda
See the `environment.yml` file for specific requirements. Aside from basic conda packages, pytorch and transformers are required for more advanced models.


To create the required environment, go to the root directory of EHRKit and run:
```
conda env create -f environment.yml --name <ENV_NAME>
```

For local LiLY lab users on tangra, setup will work a little differently:
```
pip install nltk
pip install pymysql
pip install requests
pip install gensim
pip install torch
pip install scikit-learn
pip install spacy
python -m spacy download en_core_web_sm
pip install -U pip setuptools wheel
pip install -U spacy[cuda102]
pip install transformers
```

#### Environment Option 2: using virtualenv
```
cd EHRKit
python3 -m venv ehrvir/
source ehrvir/bin/activate
pip install -r requirements.txt
```
Then you are good to go!

### Testing

You can test your installation (assuming you're in the `/EHRKit/` folder) and get familiar with the library through `tests/`. Note that this will only work with the sql mimic database setup.

```
python -m spacy download en_core_web_sm #some spacy extras must be downloaded
python -m tests/tests.py
# If you want to run all the tests, including the longer tests
python -m test/all_tests.py
```


Most of the modules access the data through a sql database. The construction of the database is described in `database_readmes`

#### MIMIC
EHRKit requires Medical Information Mart for Intensive Care-III (MIMIC-III) database to be installed. This database is freely available to the public, but it requires completion of an online training course. Information on accessing MIMIC-III can be found at https://mimic.physionet.org/gettingstarted/access.

Once you have gotten access, you can put the mimic data in the folder `data`

### Pubmed
The other dataset that is required for some of the modules is the [pubmed dataset](https://www.ncbi.nlm.nih.gov/CBBresearch/Wilbur/IRET/DATASET/), this dataset contains a large number of medical articles. The required downloading and parsing is all performed in the `pubmed/` folder. First run `bash download_pubmed.sh` and then `python parse_articles.py`. This process is also detailed in the tutorial notebook for summarization: `tutorials/naiveBayes.ipynb`

### Getting started
Once the required data has been downloaded, a new user is recommended to explore the `tutorials/` folder. These tutorials cover summarization, code classification, and query extraction.
To get a new user started, there are a number of jupyter notebooks in `tutorials/`, these tutorials cover summarization, icd9 code classification, query extraction

## Toolkit 
Jupyter notebook walkthroughs for some of these packages are available in `tutorials/`. These tutorials are the best way for a novice to familiarize themselves with these works, and in the interest of consolidation, that information will not be repeated here.

In addition to these most recent models, there are a number of other packages which do not have full tutorials, as they are built for different interactions. Readmes are written out for these packages (before we switched to the tutorial model). A full list of the modules is below.


### Modules
- `summarization/` has a naive bayes model developed by Jeremy, this model is built for extractive summarization of medical text, trained on the PubMed corpus. 
- `mimic_icd9_coding/` contains a general pipeline for classifying clinical notes from the MIMIC dataset into ICD9 billing codes. These codes contain diagnoses among other information.
- `QueryExtraction/` demonstrates simple tools for performing automated query-based extraction from text, which can easily be run on MIMIC data.
- `extractiveSummarization/` contains an implementation of Lexrank for MIMIC-III and PubMed. In the future we will make a test in tests.py that runs it on an EHR. It was developed by Sanya Nijhawan, B.S. CS '20.
- `allennlp/` has scripts utilized by tests 6.1 and 6.2 in tests.py for efficiently calling functions in the allennlp library.
- `ehrkit/` contains scripts that enable interaction with MIMIC data
- `pubmed/` contains scripts for downloading the PubMed corpus of biomedical research papers. Once downloaded, the papers are stored inside this directory.
- `tests/` has tests on the MIMIC dataset (in tests.py) and the PubMed corpus (in pubmed_tests.py).
- `collated_tasks/` has a collection of tasks on MIMIC data, including extracting named entities, abbreviations, hyponyms & linked entities, machine translation, sentence segmentation, document clustering, and retrieving similar documents. It also contains auxiliary functions including retrieving notes from NOTEEVENTS.csv and creating vector representations using bag-of-words or pre-trained transformer models. Tutorials for tasks on non-MIMIC data are also available for de-identification, inference, and medical question answering. Developed by Keen during Fall 2021.


## Get involved

Please create a GitHub issue if you have any questions, suggestions, requests or bug-reports. We welcome PRs!



# Off-shelf Functions for Medical Text Processing: EHRKit-WF
If you want to process some general medical text, please check the EHRKit-WF in [wrapper_functions](https://github.com/Yale-LILY/EHRKit/tree/master/wrapper_functions). Note: you do not need MIMIC-III access for running this. We support the following key functions:

- Abbreviation Detection & Expansion
- Hyponym Detection
- Entity Linking
- Named Entity Recognition
- Translation
- Sentencizer
- Document clustering
- Similar Document Retrieval
- Word Tokenization
- Negation Detection
- Section Detection
- UMLS Concept Extraction


